from django.shortcuts import get_object_or_404, render

# Create your views here.

from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by("-created_time")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
