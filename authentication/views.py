from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
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
            form.save()
            return redirect('login')
        else:
            return HttpResponseBadRequest()