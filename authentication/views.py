from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from .forms import RegisterForm

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'GET':
        context = {
            'form': form,
        }
        return render (request, 'auth/register.html', context)
    else:
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    return redirect('login')
                else:
                    return HttpResponseBadRequest('User Not Active')
            else:
                return HttpResponseBadRequest('User Not Found')
        else:
            return HttpResponseBadRequest()

def check_username(request):
    username = request.POST.get('username')
    context = {}
    try:
        username = User.objects.get(username=username)
        if username:
            status = True
        else:
            status = False
    except Exception:
        status = False
    
    if status:
        context = {
            'status': True,
            'message': 'Username is Already Taken'
        }
    else:
        context = {
            'status': False,
            'message': 'Username Available  '
        }
    return JsonResponse(context)

def check_email(request):
    email = request.POST.get('email')
    context = {}
    try:
        email = User.objects.get(email=email)
        if email:
            status = True
        else:
            status = False
    except Exception:
        status = False
    
    if status:
        context = {
            'status': True,
            'message': 'Email is Already Registered. Please Login for this email.'
        }
    else:
        context = {
            'status': False,
            'message': ''
        }
    return JsonResponse(context)
