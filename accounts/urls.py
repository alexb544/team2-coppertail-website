from django.urls import path, reverse_lazy
from . import views
from .views import CustomLoginView, ResetPasswordView
from django.contrib.auth import views as auth_views
from .views import ContactView
app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('about/', views.about, name='about'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')
         ), 
         name='password_reset'),
   
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name = 'password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ),
         name='password_reset_confirm'),
      
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('services/', views.services_view, name='services'),
    path('account/', views.user_account, name='account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('account/add_dog/', views.add_dog, name='add_dog'),
    path('account/dog/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('account/dog/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    # Add this line:
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', views.faq_view, name='faq'),

]
