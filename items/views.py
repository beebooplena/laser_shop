from django.shortcuts import render, get_object_or_404
from .models import Item

# Create your views here.

def all_items(request):
    """ A view to be able to show all items including search queries"""

    items = Item.objects.all()

    RequestContext = {
        'items' : items,
    }

    return render(request, 'items/items.html', RequestContext)


def item_detail(request, item_id):
    """ A view to be able to show one product and it`s details"""

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item' : item,
    }

    return render(request, 'items/item_detail.html',context)

