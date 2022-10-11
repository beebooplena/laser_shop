from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    """
    Admin model for the blog
    """
    search_fields = ['title', 'post']

