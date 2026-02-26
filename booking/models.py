from django.db import models
from django.conf import settings


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dog = models.ForeignKey("accounts.Dog", on_delete=models.PROTECT)
    slot = models.OneToOneField(TimeSlot, on_delete=models.PROTECT)

    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    notes = models.TextField(blank=True)
    

class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["booking", "service"], name="uniq_booking_service"),
        ]