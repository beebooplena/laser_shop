from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
import stripe
from bag.contexts import bag_contents
from .forms import OrderingForm



def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
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
