from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("accounts/register/", views.register, name="register"),
    # path("accounts/login/", views.unsafe_login, name="login"), # FIX: comment this path out
    # path("accounts/logout/", views.unsafe_logout, name="logout"), # FIX: comment this path out
    path("post/new/", views.create_post, name="post_create"),
    path("post/<int:pk>/delete/", views.delete_post, name="post_delete"),
    path("search/", views.search, name="search"),
    ]