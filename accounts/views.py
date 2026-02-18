from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.
#def login_view(request):
   # return render(request, "accounts/login.html")


# Custom login view using Django's built-in authentication
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"  # points to the login template

