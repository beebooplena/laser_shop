from django.shortcuts import render

def profile(request):
    """
    Show the customer profile
    """
    template = 'userprofiles/profile.html'
    context = {}

    return render(request, template, context)
