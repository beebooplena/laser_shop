from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import BlogPost
from .forms import BlogForm


def show_blog(request):
    """ This will render the blog page """
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


@login_required
def adding_post(request):
    """
    Adding items to the webstore. This code
    is borrowed from the boutique ado project
    from code institute.
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
            messages.error(request,
                           'Error. Please make sure that the form is valid.')
    else:
        form = BlogForm()

    template = 'blog/add_blog.html'
    context = {
        'form': form,

    }

    return render(request, template, context)


@login_required
def edit_blog(request, pk):
    """
    Editing blogposts in the webstore.
    This code is borrowed from the
    boutique ado project from the
    code institute.
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
            messages.error(request,
                           'Error. Please ensure that the form is valid')
    else:
        form = BlogForm(instance=blog)
        messages.info(request, 'You are now editing blog post')

    template = 'blog/update_blog.html'
    context = {
        'form': form,
        'blog': blog,
        'posts': posts,
    }

    return render(request, template, context)


@login_required
def delete_blog(request, pk):

    """
    Delete post from the webstore.
    This code is inspired from the
    boutique ado project from
    code institute
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    blog = get_object_or_404(BlogPost, pk=pk)
    blog.delete()
    messages.success(request, 'Blog post was successfully deleted')
    return redirect(reverse('blog'))
