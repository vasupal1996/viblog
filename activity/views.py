from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from post.models import Post
from .models import Activity

def get_like(request):
    if request.method == 'POST':

        post_slug = request.POST.get('post_slug')

        try:

            post = Post.objects.filter(slug=post_slug)

            likes = Activity.calculate_activity(post, atype='L')

            context = {
                'status': True,
                'likes': likes,
            }
            
        except Exception:
            context = {
                'status': False,
            }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


def get_dislike(request):
    if request.method == 'POST':
        post_slug = request.POST.get('post_slug')
        try:
            post = Post.objects.get(slug=post_slug)
            dislikes = Activity.calculate_activity(post, atype='D')
            context = {
                'status': True,
                'dislikes': dislikes
            }
            
        except Exception:
            context = {
                'status': False,
            }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


def user_activity(request):
    if request.method == "POST":
        user = request.user
        post_slug = request.POST.get('post_slug')
        try:
            post = Post.objects.get(slug=post_slug)
            activity = Activity.objects.get(user=user, post=post)
            atype = activity.activity_type
            context = {
                'status': True,
                'atype': atype,
            }
            
        except Exception:
            context = {
                'status': False
            }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()
