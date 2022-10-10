from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title', 'post']
    

