from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from items.forms import EngravedForm





# Create your views here.

def show_bag(request):
    """ A view to be able to view the bag """


    return render(request, 'bag/bag.html')


def add_item_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    amount = int(request.POST.get('amount'))
    redirect_url = request.POST.get('redirect_url')
    engraved_name = str(request.POST.get('engraved_name'))
    print("****************")
    
    bag = request.session.get('bag', {})

    
    if item_id in list(bag.keys()):
        
     
        ["engraved_name"].append({engraved_name})
        
        print("*******")
        print(engraved_name)

    else:

        if item_id in list(bag.keys()):
            bag[item_id] += amount
        else:
            bag[item_id] = amount

    request.session['bag'] = bag
    print(bag)
    return redirect(redirect_url)