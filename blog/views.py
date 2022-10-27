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


def edit_blog(request, pk):
    """
    Editing blogposts in the webstore
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))
    
    posts = BlogPost.objects.all()

    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully updated the blogpost')
            return redirect(reverse('blog'))
        else:
            messages.error(request, 'Error. Please ensure that the form is valid')
    else:
        form = BlogForm(instance=blog)
        messages.info(request,'You are now editing blog post')

    template = 'blog/update_blog.html'
    context = {
        'form': form,
        'blog': blog,
        'posts': posts,
    }

    return render(request, template, context)