from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django import forms  # ✅ Fixes forms error
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post,Comment, Like # ✅ Import Post model

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# ✅ Post creation form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


# ✅ Homepage + create post + show feed
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'home.html', {'form': form, 'posts': posts})
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    liked = Like.objects.filter(post=post, user=request.user).first()
    if liked:
        liked.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect('home')

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        Comment.objects.create(
            post=post,
            user=request.user,
            content=request.POST.get("comment")
        )
    return redirect('home')