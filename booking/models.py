from django.db import models
from django.conf import settings
from django.db.models import Q


class TimeSlot(models.Model):
    start_time = models.DateTimeField(unique=True)
    end_time = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    # TODO: manually create slots based on some given business hours
        # admins will have to manually create 'slots' in the Django admin panel for now  

    def __str__(self):
        return f"{self.start_time} - {self.end_time} ({'open' if self.is_open else 'closed'})"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dog = models.ForeignKey("accounts.Dog", on_delete=models.PROTECT)
    slot = models.OneToOneField(TimeSlot, on_delete=models.PROTECT) # no double bookings
    services = models.ManyToManyField("services.Service", through="BookingService")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    # Pricing Estimations
    subtotal = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user} - {self.slot.start_time}"
    

class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
