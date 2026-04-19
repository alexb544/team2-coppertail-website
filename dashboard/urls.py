from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Services
    path('services/add/', views.add_service, name='add_service'),
    path('services/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('services/<int:pk>/delete/', views.delete_service, name='delete_service'),

    # Time Slots
    path('timeslots/add/', views.add_timeslot, name='add_timeslot'),
    path('timeslots/<int:pk>/edit/', views.edit_timeslot, name='edit_timeslot'),
    path('timeslots/<int:pk>/delete/', views.delete_timeslot, name='delete_timeslot'),
    path('timeslots/<int:pk>/toggle/', views.toggle_timeslot, name='toggle_timeslot'),

    #Bookings
    path('bookings/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('bookings/<int:pk>/delete/', views.delete_booking, name='delete_booking'),
    path('bookings/<int:pk>/status/', views.update_booking_status, name='update_booking_status'),
]
