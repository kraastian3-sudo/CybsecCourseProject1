from django.db import models
from  django.conf import settings

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

# class Unsafe_user(models.Model):
#     username = models.TextField(unique=True)
#     password = models.TextField()
#
#     @property
#     def is_authenticated(self):
#         return True
#
#     @property
#     def is_anonymous(self):
#         return False
#
#     def __str__(self):
#         return self.username
#
# class UnsafePost(models.Model):
#     author = models.ForeignKey(
#         Unsafe_user,
#         on_delete=models.CASCADE,
#         related_name="unsafe_posts"
#     )
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_time = models.DateTimeField(
#         auto_now_add=True
#     )
#
# class UnsafeComment(models.Model):
#     post = models.ForeignKey(
#         UnsafePost,
#         on_delete=models.CASCADE,
#         related_name="unsafe_comments"
#     )
#     author = models.ForeignKey(
#         Unsafe_user,
#         on_delete=models.CASCADE,
#         related_name="unsafe_comments"
#     )
#     content = models.TextField()
#     created_time = models.DateTimeField(
#         auto_now_add=True
#     )