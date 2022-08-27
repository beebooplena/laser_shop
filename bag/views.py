from django.shortcuts import render

# Create your views here.

def show_bag(request):
    """ A view to be able to view the bag """

    return render(request, 'bag/bag.html')

