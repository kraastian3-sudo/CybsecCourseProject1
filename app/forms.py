# A07:2025 - AUTHENTICATION FAILURES
# The vulnerable registration form directly saves the supplied password into Unsafe_user.password.
# Unsafe_user.password is a normal TextField and does not use Django password hashing system.
#
# FIX:
# The safe RegisterForm below uses Djangos UserCreationForm,


from django.forms import ModelForm
from .models import Unsafeuser, UnsafeComment, UnsafePost


class UnsafeRegisterForm(ModelForm):
    class Meta:
        model = Unsafeuser
        fields = ("username", "password")

class UnsafePostForm(ModelForm):
    class Meta:
        model = UnsafePost
        fields = ("title", "content")

class UnsafeCommentForm(ModelForm):
    class Meta:
        model = UnsafeComment
        fields = ("content",)


# A07:2025 - AUTHENTICATION FAILURES
# This form collects a username and password without using Django's normal AuthenticationForm.
# This is insecure because passwords should never be stored or compared as plaintext.
#
# FIX:
# The safe implementation uses Djangos own user system. Which hashes, stores and compares safely.

from django import forms


class UnsafeLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# SAFE VERSION:

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.forms import ModelForm
# from .models import Post, Comment


# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User #
#         fields = ("username", "password1", "password2")


# class PostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ("title", "content")


# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ("content",)