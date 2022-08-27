
from django.conf import settings
from items.models import Item

def bag_contents(request):

    bag_items = []
    total = 0
    item_many = 0

    if discount == True:
        new_total = total - discount_value
        new_sum = new_total + settings.STANDARD_DELIVERY_PRICE
        total_sum = new_sum
    else:
        total_sum = total + settings.STANDARD_DELIVERY_PRICE
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'item_many': item_many,
        'total_sum':total_sum
    }

    return context

        
