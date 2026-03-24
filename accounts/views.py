from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DogForm
from .models import Profile, Dog
from booking.models import Booking


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


@login_required
def user_account(request):
    profile = Profile.objects.get(user=request.user)
    dogs = profile.dogs.all() 
    bookings = Booking.objects.filter(user=request.user).order_by('slot')

    return render(request, "accounts/account_page.html", {
        'user': request.user,
        'profile': profile,
        'dogs': dogs,
        'bookings': bookings,
    })


@login_required
def edit_account(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("accounts:account")
        
    else: 
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, "accounts/edit_account.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def add_dog(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = DogForm(request.POST)

        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = profile
            dog.save()
            return redirect("accounts:account")
        
    else:
        form = DogForm()
        
    return render(request, "accounts/add_dog.html", {
        "form": form
    })


@login_required
def edit_dog(request, dog_id):
    profile = Profile.objects.get(user=request.user)
    dog = get_object_or_404(Dog, id=dog_id, owner=profile)

    if request.method == "POST":
        form = DogForm(request.POST, instance=dog)

        if form.is_valid():
            form.save()
            return redirect("accounts:account")
    else:
        form = DogForm(instance=dog)

    return render(request, "accounts/edit_dog.html", {
        "form": form,
        "dog": dog,
    })