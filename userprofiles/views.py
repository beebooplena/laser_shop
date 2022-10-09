from django.shortcuts import render, get_object_or_404
from .models import CustomerProfile
from django.contrib import messages
from checkout.models import Ordering
from .forms import CustomerProfileForm

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
