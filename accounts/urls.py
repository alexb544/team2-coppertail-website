from django.urls import path, reverse_lazy # Added reverse_lazy here
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from .views import ResetPasswordView

app_name = 'accounts'
#app_name = 'services'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:login') # Moved inside as_view()
         ),
         name='password_reset_confirm'),
         
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
     
     path('services/', views.services_view, name='services'),
]