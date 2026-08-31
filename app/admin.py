# VULNERABLE VERSION:
# COmment from here until the safe version
from django.contrib import admin
from .models import Unsafeuser, UnsafePost, UnsafeComment

admin.site.register(Unsafeuser)
admin.site.register(UnsafePost)
admin.site.register(UnsafeComment)


# SAFE VERSION:

# from django.contrib import admin

# Register your models here.

# from .models import Post

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ("title", "created_time")
#     ordering = ("-created_time",)
