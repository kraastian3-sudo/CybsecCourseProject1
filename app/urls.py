from django.urls import path

from . import views


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("accounts/register/", views.register, name="register"),
    path("post/new/", views.create_post, name="post_create")
]
