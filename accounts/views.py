from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages 
from .forms import UserRegisterForm 
from .models import Profile
from .models import Dog


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def accounts(request):
    """Display all account information (i.e. name, email, dog information)"""
    userinfo = Profile.objects.all().values()
    dogs = Dog.objects.all().values()
    context = {
            'userinfo' : userinfo,
            'dogs' : dogs,
            'page_title' : 'Coppertail Grooming',
    }
    return render(request, 'accounts/home.html', context)


