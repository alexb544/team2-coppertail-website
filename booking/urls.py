from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.booking_create, name="booking_create"),
    path("confirm/", views.booking_confirm, name="booking_confirm"),
]