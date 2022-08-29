from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from items.forms import EngravedForm





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
    
    
    #print(engrave)
    bag = request.session.get('bag', {})
    
    if item_id in bag.keys():
        for id in bag.keys():
            if id == item_id:
                new_item = {
                    'name': engrave,
                    'amount': amount
                }
                bag[id] = new_item
    else:
        new_item = {
                'name': engrave,
                'amount': amount
        }
        bag[item_id] = new_item
    request.session['bag'] = bag
    
    return redirect(redirect_url)


