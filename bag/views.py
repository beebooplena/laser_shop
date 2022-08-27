from django.shortcuts import render, redirect

# Create your views here.

def show_bag(request):
    """ A view to be able to view the bag """


    return render(request, 'bag/bag.html')


def add_item_to_bag(request, item_id,):
    """ add quantity of an item to the bag and add engraved titles to each item or items """

    amount = int(request.POST.get('amount'))
    
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += amount
        
    else:
        bag[item_id] = amount
        
    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


