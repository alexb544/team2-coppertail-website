from services.models import Service
from django.core.mail import get_connection
from django.shortcuts import render, redirect # Added redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages # added for success and other alerts
from .forms import UserRegisterForm 
from .models import Profile
from .models import Dog
from .forms import LoginForm
from django.urls import reverse_lazy


from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Check your terminal! The link is printed there."
    success_url = reverse_lazy('accounts:accounts')

    def form_valid(self, form):
        # 1. Get the email from the form
        email = form.cleaned_data.get('email')
        # 2. Find the user
        from django.contrib.auth.models import User
        user = User.objects.get(email=email)
        
        # 3. MANUALLY CREATE THE LINK
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"
        
        # 4. FORCE PRINT TO TERMINAL
        print("\n" + "="*50)
        print("MANUAL PASSWORD RESET LINK:")
        print(reset_link)
        print("="*50 + "\n")
        
        # This skips the broken 'super' method that tries to send the email
        from django.shortcuts import redirect
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
'''
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Victory! Check your terminal for the reset link."
    success_url = reverse_lazy('accounts:accounts')

   

    email_backend = 'django.core.mail.backends.console.EmailBackend'
'''
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
    # Query all personal information
    userinfo = Profile.objects.all().values()

    # Query all dogs/ dog information
    dogs = Dog.objects.all().values()
    services = Service.objects.all()

    # Pass PI an dogs into templates
    context = {
            'userinfo' : userinfo,
            'dogs' : dogs,
            'services': services,
            'page_title' : 'Coppertail Grooming',
    }

    return render(request, 'accounts/home.html', context)

def services_view(request):
    
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})

# Create your views here.
#def login_view(request):
   # return render(request, "accounts/login.html")


# Custom login view using Django's built-in authentication
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"  # points to the login template
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # Session expires when browser closes
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        # If remember_me is checked, it uses the SESSION_COOKIE_AGE from settings
        return super(CustomLoginView, self).form_valid(form)