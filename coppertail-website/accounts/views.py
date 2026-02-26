from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView

# Custom login view using Django's built-in authentication
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"  # points to your login template
