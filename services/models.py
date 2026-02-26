from django.db import models
from django.conf import settings # Add this

class Service(models.Model):
    # This line is what's missing!
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    service_name = models.CharField(max_length=80, blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.service_name if self.service_name else "Unnamed Service"