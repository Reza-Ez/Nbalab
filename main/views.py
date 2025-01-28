from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages

def home_view(request):
    return render(request, 'base/home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Edit_Profile')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    form = LoginForm()
    error = ''

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error = "Username or password is incorrect"
    return render(request, 'authentication/login.html', {'form': form, 'error': error})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('profile')

@login_required
def profile_view(request):
    return render(request, 'profile/profile.html')


def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('Edit_Profile')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'profile/editprofile.html', {'form': form})
