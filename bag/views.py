from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from items.forms import EngravedForm
import uuid




# Create your views here.

def show_bag(request):
    """ A view to be able to view the bag """


    return render(request, 'bag/bag.html')


def add_item_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    

    if request.method == 'GET':
        request.session.pop('bag')
        return redirect(request.path)
    redirect_url = request.POST.get('redirect_url')
    amount = int(request.POST.get('amount'))
    engrave = str(request.POST.get('engraved_name'))
    
   
    # print(engrave)
    bag = request.session.get('bag', {})
    
    # dict_items([('item_id', {'name': 'tow', 'amount': 4})])
    new_item = {
            'name': engrave,
            'amount': amount
    }
    bag[get_id()] = new_item
        
    request.session['bag'] = bag
  
    
    return redirect(redirect_url)


def get_id():
    """
    Generate a random, unique order number using UUID
    """
    return uuid.uuid4().hex.upper()


