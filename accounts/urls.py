from django.urls import path
from . import views
from .views import CustomLoginView
#from .views import ChangePasswordView

# App namespace (for URL reversing)
app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
