
from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item

def bag_contents(request):

    bag_items = []
    total = 0
    item_many = 0
    delivery = settings.STANDARD_DELIVERY_PRICE
    bag = request.session.get('bag', {})

    for item_id, amount in bag.items():
        item = get_object_or_404(Item, pk=item_id)
        if item.discount is True:
            total += amount * (item.price - item.discount_value) + delivery
        else:
            total += amount * item.price + delivery
            item_many += amount
       

        bag_items.append({
            'item_id': item_id,
            'amount': amount,
            'item': item,

        })

            
    sum_total = total
           


    context = {
        'bag_items': bag_items,
        'total': total,
        'item_many': item_many,
        'delivery': delivery,
        'sum_total': sum_total,
        
    }
    print('bag_items')

    return context

        
