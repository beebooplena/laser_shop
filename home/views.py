from django.shortcuts import render


def homeindex(request):
    """ A view to be able to return index.html"""

    return render(request, 'home/index.html')
