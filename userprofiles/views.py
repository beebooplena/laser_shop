from django.shortcuts import render

def userprofile(request):
    """
    Show the customer profile
    """
    template = 'userprofile/userprofile.html'
    context = {}

    return render(request, template, context)
