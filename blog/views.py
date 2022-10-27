from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import BlogPost
from .forms import BlogForm


def show_blog(request):
    """ This will render blog page """
    posts = BlogPost.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/blog.html', context)


def blog_post(request, pk):
    """ This will render blog page """
    posts = BlogPost.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/blog_post.html', context)



def adding_post(request):
    """
    Adding items to the webstore
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))
    

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully added a blog post')
            return redirect(reverse('blog'))
        else:
            messages.error(request, 'Error. Please make sure that the form is valid.')
    else:
        form = BlogForm()

    template = 'blog/add_blog.html'
    context = {
        'form': form,
        
    }

    return render(request, template, context)