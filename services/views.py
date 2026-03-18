from django.shortcuts import render
from .models import Service

def services(request):
    """View for Services page. Display all services and information"""
    services = Service.objects.all().values()
    context = {
        'services' : services,
    }
    return render(request, 'services/services.html', context)