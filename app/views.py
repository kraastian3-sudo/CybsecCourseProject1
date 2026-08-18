from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
# Create your views here.

from .models import Post
from .forms import RegisterForm

def post_list(request):
    posts = Post.objects.all().order_by("-created_time")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = RegisterForm

    return render(request, "registration/register.html", {"form": form})
