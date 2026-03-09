from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('register/', views.register, name='register'),
]
