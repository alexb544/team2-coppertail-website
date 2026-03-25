from django.urls import path, reverse_lazy
from . import views
from .views import CustomLoginView, ResetPasswordView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('register/', views.register, name='register'),


path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:login')
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
]
