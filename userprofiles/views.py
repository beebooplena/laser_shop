from django.shortcuts import render, get_object_or_404

from .models import CustomerProfile

def userprofile(request):
    """
    Show the customer profile
    """
    customer = get_object_or_404(CustomerProfile, user=request.user)
    template = 'userprofile/userprofile.html'
    context = {
        'customer': customer,
    }

    return render(request, template, context)
