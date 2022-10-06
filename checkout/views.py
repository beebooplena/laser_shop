from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderingForm

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There`s nothing in your bag at the moment")
        return redirect(reverse('items'))
    
    ordering_form = OrderingForm()
    template = 'checkout/checkout.html'
    context = {
        'ordering_form': ordering_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
