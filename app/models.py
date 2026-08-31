# from django.db import models

# A07:2025 - AUTHENTICATION FAILURES
# The vulnerable user model stores the password directly in a
# TextField without hashing it.
# FIX:
# Djangos User model and authentication system  are the fix for this vulnerability.
# Comment the unsafe classes out

# class Unsafeuser(models.Model):
#     username = models.TextField(unique=True)
#     password = models.TextField()

#     @property
#     def is_authenticated(self):
#         return True

#     @property
#     def is_anonymous(self):
#         return False

#     def get_session_auth_hash(self):
#         return self.password

#     last_login = models.DateTimeField(
#         null=True,
#         blank=True
#         )

#     def __str__(self):
#         return self.username


# A07:2025 - AUTHENTICATION FAILURES.
# The Unsafe_user.password field stores plaintext passwords.

# class UnsafePost(models.Model):
#     author = models.ForeignKey(
#         Unsafeuser,
#         on_delete=models.CASCADE,
#         related_name="unsafe_posts"
#     )
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class UnsafeComment(models.Model):
#     post = models.ForeignKey(
#         UnsafePost,
#         on_delete=models.CASCADE,
#         related_name="unsafe_comments"
#     )
#     author = models.ForeignKey(
#         Unsafeuser,
#         on_delete=models.CASCADE,
#         related_name="unsafe_comments"
#     )
#     content = models.TextField()
#     created_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
       # return f"Comment by {self.author} on {self.post}"


# SAFE VERSION:
# Django's AUTH_USER_MODEL provides the proper authentication
# system and password hashing. Posts and comments reference
# that authenticated user instead of the unsafe custom user.

from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"