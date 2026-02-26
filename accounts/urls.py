from django.urls import path
from . import views
from .views import CustomLoginView
#from .views import ChangePasswordView

# App namespace (for URL reversing)
app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
   # in accounts/urls.py
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('register/', views.register, name='register'),
    #path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
