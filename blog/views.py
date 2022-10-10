from django.shortcuts import render

def show_blog(request):
    """ This will render blog """



    context = {
        
    }

    return render(request, 'blog/blog.html', context)
