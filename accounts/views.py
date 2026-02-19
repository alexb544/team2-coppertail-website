from django.shortcuts import render
from .models import Profile
from .models import Dog

def accounts(request):
    """Display all account information (i.e. name, email, dog information)"""
    # Query all personal information
    userinfo = Profile.objects.all().values()

    # Query all dogs/ dog information
    dogs = Dog.objects.all().values()

    # Pass PI an dogs into templates
    context = {
            'userinfo' : userinfo,
            'dogs' : dogs,
            'page_title' : 'Coppertail Grooming',
    }

    return render(request, 'accounts/home.html', context)
