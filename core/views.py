

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from .forms import UserForm, UserProfileForm, UserImageForm
from post.models import Post

@login_required
def profile(request, username):
    user = request.user
    if request.method == 'GET':
        context = {
            'form': UserForm(instance=user),
            'userform': UserProfileForm(instance=user.userprofile),
            'user': user,
            'image': user.userprofile.profile_image,
        }
        return render(request, 'core/profile.html', context)
    else:
        form = UserForm(request.POST)
        userform = UserProfileForm(request.POST)
        if form.is_valid() and userform.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.userprofile.dob = userform.cleaned_data.get('dob')
            user.userprofile.state = userform.cleaned_data.get('state')
            user.userprofile.country = userform.cleaned_data.get('country')
            user.userprofile.mobile = userform.cleaned_data.get('mobile')
            user.userprofile.alternate_email = userform.cleaned_data.get('alternate_email')
            user.userprofile.intro_slogan = userform.cleaned_data.get('intro_slogan')
            user.save()
            return redirect('post:home')
        else:
            return redirect('login')


@login_required
def image_profile(request, username):
    if request.method == "POST":
        user = request.user
        image = request.FILES.get('file')
        user.userprofile.profile_image = image
        user.save()
        context = {
            'user': user.userprofile,
        }
        html = ''
        html = '{0}{1}'.format(html, render_to_string('core/profile_image.html', context))
        return HttpResponse(html)
    else:
        user = request.user
        image_url = User.userprofile.profile_image.url
        context = {
            'status': True,
            'url': image_url
        }
        return JsonResponse(context)

@login_required
def list_posts(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        posts = Post.get_posts(user)
        context = {
            'posts': posts
        }
        return render(request, 'core/list_post.html', context)