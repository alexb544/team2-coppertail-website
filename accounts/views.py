from django.shortcuts import render, redirect
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

#password reset imports:
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User


from .forms import UserRegisterForm, LoginForm
from .models import Profile, Dog
from services.models import Service


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Session expires when browser closes
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """View to handle password reset requests and print the link to the terminal"""
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Check your terminal! The reset link is printed there."
    success_url = reverse_lazy('accounts:accounts')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            # Look up the user by email
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create the link for local testing
            #reset_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"

            domain = self.request.get_host()
            reset_link = f"http://{domain}/password-reset-confirm/{uid}/{token}/"
            
            # Print to terminal for the developer to see
            print("\n" + "="*50)
            print("MANUAL PASSWORD RESET LINK:")
            print(reset_link)
            print("="*50 + "\n")
            
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except User.DoesNotExist:
            messages.error(self.request, "No user found with that email address.")
            return redirect('accounts:password_reset')

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

def services_view(request):
    """Standalone view to display all grooming services"""
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})

