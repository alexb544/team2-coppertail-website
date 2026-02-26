from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Booking, BookingService, TimeSlot

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        "start_time", 
        "end_time", 
        "is_open"
    )
    search_fields = ()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "user", 
        "dog", 
        "slot", 
        "status",
        "subtotal",
        "total", 
        "notes", 
        "created_at"
    )
    search_fields = () 
