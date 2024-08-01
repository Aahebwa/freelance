from django.shortcuts import render, redirect
from .models import Post, UserProfile
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def community(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'community.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/')  # Replace with the name of your community view
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, 'Invalid Username or Password')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Wrong Username or Password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')
