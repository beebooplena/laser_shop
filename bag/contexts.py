
from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item



def bag_contents(request):
    """
    Shopping bag, code inspired by boutique ado code institute project.
    """
    bag_items = []
    total = 0
    item_many = 0
    sumup = None

    delivery = settings.STANDARD_DELIVERY_PRICE
    bag = request.session.get('bag', {})

    for item_id, values in bag.items():
        item = get_object_or_404(Item, pk=values['id'])
        amount = values.get('amount')
        if item.discount is True:
            total += amount * (item.price - item.discount_value)
            item_many += amount
            sumup = total + delivery
        else:
            total += amount * item.price
            item_many += amount
            sumup = total + delivery
        

        

        bag_items.append({
            'item_id': item_id,
            'amount': amount,
            'item': item,
            'engraved_name': values.get('name'),
            
            })
        print("*********")
        print(bag)
        print("*********")
        
    sum_total = sumup
    context = {
        'bag_items': bag_items,
        'total': total,
        'item_many': item_many,
        'delivery': delivery,
        'sum_total': sum_total,
    }

    return context