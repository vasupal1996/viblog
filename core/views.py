from PIL import Image
from bs4 import BeautifulSoup
import os
import django

from django.core.files import File

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from django.forms import formset_factory

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from django.template.loader import render_to_string

from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import UserProfileForm1, UserProfileForm2, UserImageForm
from post.models import Post

from viblog.settings import MARKDOWNX_MARKDOWNIFY_FUNCTION
from django.utils.module_loading import import_string


EXTENSION = ['jpg', 'png', 'jpeg']

@login_required
def profile(request, username):
    user = request.user
    if request.method == 'GET':
        context = {
            'form': UserProfileForm1(instance=user),
            'userform': UserProfileForm2(instance=user.userprofile),
            'user': user,
            'image': user.userprofile.get_profile_picture_url,
        }
        return render(request, 'core/profile.html', context)
    else:
        userprofileform1 = UserProfileForm1(request.POST)
        userprofileform2 = UserProfileForm2(request.POST)
        if userprofileform1.is_valid() and userprofileform2.is_valid():
            try:
                if User.objects.get(username=user.username) is not None:
                    user.first_name = userprofileform1.cleaned_data.get('first_name')
                    user.last_name = userprofileform1.cleaned_data.get('last_name')
                    user.userprofile.dob = userprofileform2.cleaned_data.get('dob')
                    user.userprofile.state = userprofileform2.cleaned_data.get('state')
                    user.userprofile.country = userprofileform2.cleaned_data.get('country')
                    user.userprofile.mobile = userprofileform2.cleaned_data.get('mobile')
                    user.userprofile.alternate_email = userprofileform2.cleaned_data.get('alternate_email')
                    user.save()
                    return redirect('core:profile', username = user.username)
                else:
                    return HttpResponseBadRequest()
            except Exception:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


@login_required
def image_profile(request, username):
    user = request.user
    if request.method == "POST":
        image = request.FILES.get('file')
        file_path = settings.BASE_DIR + settings.MEDIA_URL + 'profile-images/' + user.username
        user.userprofile.profile_image = image
        user.save()
        file_name = user.userprofile.profile_image.url
        file_name = file_name.split('/')[-1]
        im = Image.open(file_path + '/' + file_name)
        width, height = (im.size)
        if width > height:
            x = 0 + int((width-height))/2
            y = 0
            w = width - int((width-height))/2
            h = height
        elif height > width:
            x = 0
            y = 0 + (height - width)/2
            w = width
            h = height - (height - width)/2
        else:
            pass
        try:
            im = im.crop((x, y, w, h))
        except: 
            pass
        im.save(file_path + '/' + file_name)
        return HttpResponse(True)
    else:
        image_url = user.userprofile.get_profile_picture_url
        context = {
            'status': True,
            'url': image_url
        }
        return JsonResponse(context)

@login_required
def list_posts(request, username):
    if request.method == 'GET':
        user = request.user
        post_list = Post.get_posts(user)
        paginator = Paginator(post_list, 10) # Show 25 contacts per page
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
        }
        return render(request, 'core/list_post.html', context)


# def create_thumbnail(request):
    # slug = 'samsung-galaxy-note8-hands-on-review'
    # post = get_object_or_404(Post, slug=slug)
    # if post:
    #     markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)
    #     content = BeautifulSoup(markdownify(post.content), "html5lib")
    #     try:
    #         img_link = content.findAll('img')[0].get('src')
    #         file_path = settings.BASE_DIR + img_link
    #         file_full_name = img_link.split('/')[-1]
    #         file_name, extension = file_path.split('.')
    #         file_name = file_name.split('/')[-1]
    #         try:
    #             if extension in EXTENSION:
    #                 username = post.author.username
    #                 new_file_path = settings.BASE_DIR + settings.STATIC_URL + 'media' + '/' + settings.DRACEDITOR_UPLOAD_PATH + post.author.username + '/' + post.slug + '/'
    #                 new_file_name = new_file_path + file_name + '-thumbnail'
    #                 if not os.path.exists(new_file_path):
    #                     print ('HERE')
    #                     os.makedirs(new_file_path)
    #                 im = Image.open(file_path)
    #                 width, height = (im.size)
    #                 if width > height:
    #                     x = 0 + int((width-height))/2
    #                     y = 0
    #                     w = width - int((width-height))/2
    #                     h = height
    #                 elif height > width:
    #                     x = 0
    #                     y = 0 + (height - width)/2
    #                     w = width
    #                     h = height - (height - width)/2
    #                 else:
    #                     pass
    #                 im = im.crop((x, y, w, h))
                  
    #                 width, height = (im.size)
    #                 im.save(new_file_name + '.' + extension)
                    
    #         except:
    #             raise Exception('Please Upload Correcct Image Format')
    #     except:
    #         img_link = 'http://howtorecordpodcasts.com/wp-content/uploads/2012/10/YouTube-Background-Pop-4.jpg'
        
    #     context = {
    #         'post': post, 
    #         'username': post.author.username,
    #         'file': new_file_name + '.' + extension,
    #     }
        
    #     return render(request, 'core/example.html', context)