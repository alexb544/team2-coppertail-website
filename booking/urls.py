from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('new/', views.booking_create, name='booking_create'),
    path('slots-json/', views.booking_slots_json, name='booking_slots_json'),
    path('confirm/', views.booking_confirm, name='booking_confirm'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
]