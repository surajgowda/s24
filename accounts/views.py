from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form':UserCreateForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form':UserCreateForm, 'error':'username already exists!'})

        else:
            return render(request, 'signupaccount.html', {'form':UserCreateForm, 'error':'Password doesn\'t match'})


@login_required
def logoutaccount(request):
    logout(request)
    return redirect('index')

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginaccount.html', {'form':AuthenticationForm, 'error': 'No user found'})
        else:
            login(request, user)
            return redirect('index')


# Create your views here.
