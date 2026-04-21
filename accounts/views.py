from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DogForm, LoginForm
from .models import Profile, Dog
from services.models import Service
from booking.models import Booking
from .forms import ContactForm
from django.views.generic import FormView 
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse 

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


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
    services = Service.objects.all()
    context = {
            'userinfo' : userinfo,
            'dogs' : dogs,
            'services': services,
            'page_title' : 'Coppertail Grooming',
    }
    return render(request, 'accounts/home.html', context)


@login_required
def user_account(request):
    profile = Profile.objects.get(user=request.user)
    dogs = profile.dogs.all() 
    bookings = Booking.objects.filter(user=request.user, status='CONFIRMED').order_by('slot')
    #bookings = Booking.objects.filter(user=request.user).order_by('slot')
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
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile) 
    
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
    
    return render(request, "accounts/add_dog.html", {"form": form})


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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Check your Email! The reset link is printed there."
    success_url = reverse_lazy('accounts:accounts')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = self.request.get_host()
            reset_link = f"http://{domain}/password-reset-confirm/{uid}/{token}/"
            print("\n" + "="*50)
            print("MANUAL PASSWORD RESET LINK:")
            print(reset_link)
            print("="*50 + "\n")
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except User.DoesNotExist:
            messages.error(self.request, "No user found with that email address.")
            return redirect('accounts:password_reset')


def services_view(request):
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})

def about(request):
    return render(request, 'accounts/about.html')

class ContactView(FormView):
    template_name = 'accounts/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('accounts:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        user_email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        
        subject = f"Coppertail Inquiry from {name}"
        body = f"From: {user_email}\n\nMessage:\n{message}"

        # Using EmailMessage class allows for the reply_to argument
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email='noreply@coppertail.com',
            to=['groomingcoppertail@gmail.com'],
            reply_to=[user_email], 
        )

        try:
            email.send() # This calls the actual send method
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
            
        messages.success(self.request, "Success! We'll bark back as soon as we can.")
        return super().form_valid(form)

def faq_view(request):
    faqs = [
        {
            "q": "What vaccinations does my dog need?",
            "a": "For the safety of all our furry guests, we require proof of Rabies, Distemper, and Bordetella vaccinations."
        },
        {
            "q": "How long does a grooming session take?",
            "a": "Depending on the size of the dog and the condition of their coat, the time will vary."
        },
        {
            "q": "Do you groom aggressive dogs?",
            "a": "We handle every dog with care. However, for the safety of our staff, we ask that you disclose any history of aggression so we can determine the best approach."
        },
        {
            "q": "Where are you located in Lakeland?",
            "a": "We are located at 119 Allamanda Drive, Lakeland FL 33803"
        },
    ]
    return render(request, 'accounts/faq.html', {'faqs': faqs})