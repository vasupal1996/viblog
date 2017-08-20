import os
import json
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Post
from .forms import CreatePost

from activity.models import Activity

from draceditor.utils import LazyEncoder


def home(request):
    user = request.user
    # favourites = Favourites.objects.filter(user=user)
    # posts = Tag.objects.filter(tag__icontains=favourites)
    posts = Post.objects.all().order_by('-date_created')
    context = {
        'posts': posts,
        'user': user,   
    }
    return render(request, 'post/index.html', context)

def create(request):
    form = CreatePost(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        print ('here1')
        if form.is_valid():
            print ('here2')
            post = Post()
            post.author = request.user
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content') 
            tags = form.cleaned_data.get('tags')
            status = form.cleaned_data.get('status')
            if status in [Post.PUBLISHED, Post.DRAFT]:
                post.status =  status
            post.save()
            post.create_tags(tags)
    else:
        return render(request, 'post/create.html', {'form': form})


def edit(request, slug=None):
    tags = ''
    if slug:
        post = get_object_or_404(Post, slug=slug)
        for tag in post.get_tags():
            tags = '{0} {1},'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        post = Post(author=request.user)

    if post.author.id != request.user.id:
        return redirect('post:home')

    if request.POST:
        form = CreatePost(request.POST, instance=post)
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            form.save()
            post = get_object_or_404(Post, slug=slug)
            post.create_tags(tags)
            return redirect('post:home')
    else:
        form = CreatePost(instance=post, initial={'tags': tags})
    return render(request, 'post/edit.html', {'form': form})
    

def api(request):
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
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.DRACEDITOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
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
            print ('here2')
            return redirect('post:home')

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
        print ('here')        
        post.status = 'P'
        post.save()
        return redirect('post:home')
    else:
        return HttpResponseBadRequest()


@login_required
def delete(request, slug):
    print ('into function')
    post = get_object_or_404(Post, slug=slug)
    print ('HERE')
    post.delete()
    return redirect ('post:home')

@login_required
def comment(request, slug):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, slug=slug)
        print (request.POST)
        comment = request.POST.get('comment')
        Post.create_comments(post, user, comment)
        return redirect('post:detail', slug=slug)
    else:
        return HttpResponseBadRequest