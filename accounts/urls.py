from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', CustomLoginView.as_view(next_page='accounts:accounts'), name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.user_account, name='account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('account/add_dog/', views.add_dog, name='add_dog'),
    path('account/dog/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
]
