from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Item
from .forms import ItemForm


def all_items(request):
    """ This code is borrowed from boutique
    Ado project.
    A view to show all items, including search queries """

    items = Item.objects.all()

    query = None

    if request.GET:
        if 's' in request.GET:
            query = request.GET['s']
            if not query:
                messages.error(request,
                               "You didn`t write any search words.")
                return redirect(reverse('items'))

            queries = Q(name__icontains=query) | \
                Q(description__icontains=query)
            items = items.filter(queries)
    context = {
        'items': items,
        'search_items': query,
    }

    return render(request, 'items/items.html', context)


def item_detail(request, item_id):
    """ A view to be able to show one product and it`s details"""

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'items/item_detail.html', context)


@login_required
def adding_item(request):
    """
    Adding items to the webstore
    This code is borrowed from the
    boutique ado project from
    the code institute.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully added an Item')
            return redirect(reverse('adding_item'))
        else:
            messages.error(request,
                           'Error. Please make sure that the form is valid.')
    else:
        form = ItemForm()

    template = 'items/adding_item.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_item(request, item_id):
    """
    Editing items in the webstore.
    This code is borrowed from the
    boutique ado project from
    the code institute.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully updated the item')
            return redirect(reverse('item_detail', args=[item.id]))
        else:
            messages.error(request,
                           'Error. Please ensure that the form is valid')
    else:
        form = ItemForm(instance=item)
        messages.info(request, f'You are now editing {item.name}')

    template = 'items/edit_item.html'
    context = {
        'form': form,
        'item': item,
    }

    return render(request, template, context)


@login_required
def delete_item(request, item_id):

    """
    Delete item from the webstore.
    This code is borrowed from the
    boutique ado project from
    the code institute.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Item was successfully deleted')
    return redirect(reverse('items'))
