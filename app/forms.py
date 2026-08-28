from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User #
        fields = ("username", "password1", "password2")

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


# from django.forms import ModelForm
# from .models import Unsafe_user
#
# class UnsafeRegisterForm(ModelForm):
#     class Meta:
#         model = Unsafe_user
#         fields = ("username", "password")

# from django import forms
#
# class UnsafeLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(
#         widget=forms.PasswordInput
#     )