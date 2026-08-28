from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import Post
from .forms import RegisterForm, PostForm, CommentForm

def post_list(request):
    posts = Post.objects.all().order_by("-created_time")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect("post_detail", pk=post.pk)

    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {"post": post, "form": form})

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

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})

# --------------------------------------------------
# INTENTIONALLY VULNERABLE LOGIN VIEW
# --------------------------------------------------

# from django.contrib.auth import login
# from .forms import UnsafeLoginForm
#
# def unsafe_login(request):
#     if request.method == "POST":
#         form = UnsafeLoginForm(request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#
#             user = authenticate(
#                 request,
#                 username=username,
#                 password=password
#             )
#
#             if user is not None:
#                 login(request, user,
#                       backend="blog.backends.UnsafeAuthBackend")
#                 return redirect("post_list")
#
#             form.add_error(
#                 None,
#                 "Invalid username or password."
#             )
#     else:
#         form = UnsafeLoginForm()
#
#     return render(
#         request,
#         "registration/login.html",
#         {"form": form}
#     )