import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
from bag.contexts import bag_contents
from items.models import Item
from .models import Ordering, OrderingLineItem
from .forms import OrderingForm


@require_POST
def cache_checkout_data(request):
    """
    This function will check if the user checked the
    save info box.
    This code is borrowed from code institute, from the
    project boutique ado.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request,'So sorry, Your payment \
            cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_info = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'mobile_number': request.POST['mobile_number'],
            'city': request.POST['city'],
            'zip_code': request.POST['zip_code'],
            'street_address': request.POST['street_address'],
            'country': request.POST['country'],
        }
        ordering_form = OrderingForm(form_info)
        if ordering_form.is_valid():
            ordering = ordering_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            ordering.stripe_pid = pid
            ordering.original_bag = json.dumps(bag)
            ordering.save()
            for item_id, values in bag.items():
                try:
                    item = get_object_or_404(Item, pk=values['id'])
                    ordering_line_item = OrderingLineItem(
                        ordering=ordering,
                        item=item,
                        amount=values.get('amount'),
                        name_engraved=values.get('name')
                        
                    )
                    ordering_line_item.save()
                except Item.DoesNotExist:
                    messages.error(request, (
                        "Couldn`t find items in your bag in our database."
                        "Please contact us and we will help you.")
                        )
                    ordering.delete()
                    return redirect(reverse('show_bag'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[ordering.ordering_number]))
        else:
            messages.error(request, 'An error occured with your form. \
                Please try again')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There`s nothing in your bag at the moment")
            return redirect(reverse('items'))
        
        bag_current = bag_contents(request)
        total = bag_current['sum_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        
        ordering_form = OrderingForm()

    if not stripe_public_key:
        messages.warning(request, 'stripe public key is missing. \
            Please set it in your environment')

    template = 'checkout/checkout.html'
    context = {
        'ordering_form': ordering_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, ordering_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    ordering = get_object_or_404(Ordering, ordering_number=ordering_number)
    messages.success(request, f'You successfully ordered! \
        Your order number is {ordering_number}. A confirmation \
            email will be sent to {ordering.email}')
    if 'bag' in request.session:
        del request.session['bag']
    template = 'checkout/checkout_success.html'
    context = {
        'ordering': ordering,
    }

    return render(request, template, context)
