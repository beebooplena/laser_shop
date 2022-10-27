from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Ordering
from .models import CustomerProfile


from .forms import CustomerProfileForm

@login_required
def profile(request):
    """
    Show the customer profile
    """
    profile = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your customer \
                profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please try again')
    else:
        form = CustomerProfileForm(instance=profile)
    orders = profile.orders.all().order_by('-time')
    
    template = 'userprofile/profile.html'
    context = {
        'form': form,
        'orders': orders,
        
    }

    return render(request, template, context)


@login_required
def history_order(request, ordering_number):
    order = get_object_or_404(Ordering, ordering_number=ordering_number)

    messages.info(request, (
        f'This is a past confirmation for order number {ordering_number}'
        ' A confirmation email was sent on the order date'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)