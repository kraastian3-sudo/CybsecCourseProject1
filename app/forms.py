from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
