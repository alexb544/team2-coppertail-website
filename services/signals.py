""""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from .models import Service

User = get_user_model()
@receiver(post_save, sender=User)
def create_user_services(sender, instance, created, **kwargs):
    if created:
        Service.objects.create(user=instance)
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service  # This imports the model from models.py

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_services(sender, instance, created, **kwargs):
    if created:
        # This creates a record in the Service table for the new user
       Service.objects.create(
            user=instance, 
            service_name="Standard Groom", 
            base_price=0.00,  # This fixes the NOT NULL error
            description="Default service created at signup"
        )