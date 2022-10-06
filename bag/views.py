from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from items.models import Item





globalId = 5000

# Create your views here.

def show_bag(request):
    """ A view to be able to view the bag """


    return render(request, 'bag/bag.html')


def add_item_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    global globalId
    item = get_object_or_404(Item, pk=item_id)
    

    if request.method == 'GET':
        request.session.pop('bag')
        return redirect(request.path)
    redirect_url = request.POST.get('redirect_url')

    
    
    while True:
        amount = int(request.POST.get('amount'))
        try:
            amount = int(amount)
            print("jaaaaa")
            break
            
        except Exception as e:
            messages.error(request, (
            'Error! No strings allowed'))

            return HttpResponse(status=500)
   
    engrave = str(request.POST.get('engraved_name'))
    
    if len(engrave) >= 10:
        messages.error(request, (
            'Error! Your name was over 10 caracters'))
        return redirect(redirect_url)
    else:
    
        print("MMMMMMM")
    
        bag = request.session.get('bag', {})
        new_item = {
            'name': engrave,
            'amount': amount,
            'id': item_id
            }
        bag[globalId] = new_item
        globalId += 1
        messages.success(request, f'You successfully added {item.name} in the bag')
        
        request.session['bag'] = bag
        
  
    
        return redirect(redirect_url)





def update_bag(request, item_id):
    
   
    amount = int(request.POST.get('amount'))
    engrave = str(request.POST.get('engraved_name'))
    if len(engrave) >= 10:
        messages.error(request, (
            'Error! Your name was over 10 caracters'))
        return redirect(redirect_url)
    else:

        bag = request.session.get('bag', {})
        old_item = bag[item_id]
    
        new_item = {
            'name': engrave,
            'amount': amount,
            'id': old_item['id']
            }
    
        bag[item_id] = new_item
        messages.success(request, 'You successfully updated your bag')
    

        
        
        
        request.session['bag'] = bag
  
    
        return redirect('show_bag')

def remove_bag(request, item_id):
    """Remove the item from the shopping bag"""
    
    bag = request.session.get('bag', {})

        
    bag.pop(item_id)
    messages.success(request, 'You successfully deleted your bag')
    request.session['bag'] = bag
        
        
    return redirect('show_bag')

    