from django.shortcuts import render
from .models import BlogPost


def show_blog(request):
    """ This will render blog page """
    posts = BlogPost.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/blog.html', context)
