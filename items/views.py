from django.shortcuts import render
from .models import Item

# Create your views here.

def all_items(request):
    """ A view to be able to show all items including search queries"""

    items = Item.objects.all()

    RequestContext = {
        'items' : items,
    }

    return render(request, 'items/items.html', RequestContext)

