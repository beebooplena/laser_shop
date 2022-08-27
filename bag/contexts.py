
from django.conf import settings
from items.models import Item

def bag_contents(request):

    bag_items = []
    total = 0
    item_many = 0

  

   
    context = {
        'bag_items': bag_items,
        'total': total,
        'item_many': item_many,
        
    }

    return context

        
