import os
import json
import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Post
from .forms import CreatePost

from activity.models import Activity

from draceditor.utils import LazyEncoder


def home(request):
    user = request.user
    post_list = Post.objects.all().filter(status='P')#.order_by("-date_created")
    paginator = Paginator(post_list, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        return HttpResponseBadRequest('No Page Found')
    
    context = {
        'posts': posts,
        'user': user,
    }
    return render(request, 'post/index.html', context)


# def load_post(request):
#     user = request.user
#     page = int(request.POST.get('next_page_number'))
#     post_list = Post.objects.all().filter(status='P').order_by("-date_created")
#     paginator = Paginator(post_list, 1) # Show 25 contacts per page
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         posts = paginator.page(paginator.num_pages)
#         return HttpResponseBadRequest('No Page Found')

#     context = {
#         'posts': posts,
#     }
#     return render(request, 'includes/post.html', context)

@login_required
def draft_or_publish_post(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            form = CreatePost(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                try:
                    new_post = Post.objects.get(title=title, author=user)
                except:
                    new_post = Post()
                new_post.title = form.cleaned_data.get("title").strip()
                new_post.content = form.cleaned_data.get('content')
                new_post.author = request.user
                status = form.cleaned_data.get('status')
                if status in [Post.PUBLISHED, Post.DRAFT]:
                    new_post.status = status
                else:
                    new_post.status = Post.DRAFT
                new_post.save()
                tags = form.cleaned_data.get('tags')
                if tags:
                    new_post.create_tags(tags)
                return redirect('core:list_posts', username=user.username)
        else:
            return HttpResponseBadRequest('Cannot Process Request')
    else:
        return redirect('login')


def create_or_edit_post(request, slug=None):
    user = request.user
    tags = ''
    if request.method == 'GET':
        if user.is_authenticated:
            if slug:
                post = get_object_or_404(Post, slug=slug, author=user)
                if post:
                    for tag in post.get_tags():
                        tags = '{0} {1},'.format(tags, tag.tag)
                    tags = tags.strip()
                else:
                    return HttpResponseBadRequest('Post Does Not Exists')
                form = CreatePost(instance=post, initial={'tags':tags})
                return render(request, 'post/edit.html', {'form':form})
            else:
                form = CreatePost()
                return render(request, 'post/create.html', {'form':form})
        else:
            return redirect('login')
    else:
        return HttpResponseBadRequest("Invalid Request")
    
def image_upload(request):
    if request.method == 'POST' and request.is_ajax():
        
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(data, content_type='application/json', status=405)

            img_key = uuid.uuid4().hex[:10]
            img_path = settings.DRACEDITOR_UPLOAD_PATH + str(request.user.username) 

            img_uuid = "{0}-{1}".format(img_key, image.name.replace(' ', '-'))
            tmp_path = os.path.join(img_path, img_uuid)

            def_path = default_storage.save(tmp_path, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))

def detail(request, slug):
    user = request.user
    post = get_object_or_404(Post, slug=slug)
    tags = ''
    for tag in post.get_tags():
        tags = '{0} {1},'.format(tags, tag.tag)
    comments = post.get_comment()
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'user': user,
    }
    return render(request, 'post/list.html', context)


def activity(request):
    if request.method == 'POST':
        user = request.user
        post_slug = request.POST.get('post_slug')
        post = Post.objects.get(slug=post_slug)
        actype = request.POST.get('atype')
        status = True
        like = Activity.objects.filter(activity_type = Activity.LIKE, post=post, user=user)
        dislike = Activity.objects.filter(activity_type = Activity.DISLIKE, post=post, user=user)
        
        if actype in Activity.LIKE:
            atype = Activity.LIKE      
            if not dislike:
                if like:
                    like.delete()
                    status = False
            else:
                 dislike.delete()

        elif actype in Activity.DISLIKE:
            atype = Activity.DISLIKE
            if not like:
                if dislike: 
                    dislike.delete() 
                    status = False   
            else:
                like.delete()
        else:
            return HttpResponseBadRequest()

        if status:
            Activity.create_activity(user, post, atype)
        
        context ={
        }
    
        count = Activity.calculate_activity(post, atype)
        context = {
            'status': True,
            'count': count,
        }
        return JsonResponse(context)

@login_required
def publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.status is 'D':       
        post.status = 'P'
        post.save()
        return redirect('core:list_posts', username=request.user.username)
    else:
        return HttpResponseBadRequest()


@login_required
def delete(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)
        post.delete()
    except Exception:
        pass
    return redirect('core:list_posts', username=request.user.username)

@login_required
def comment(request, slug):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, slug=slug)
        try:
            user = User.objects.get(username=user.username)
            comment = request.POST.get('comment')
            Post.create_comments(post, user, comment)
            return redirect('post:detail', slug=slug)
        except Exception:
            return redirect('post:detail', slug=slug)
    else:
        return HttpResponseBadRequest()