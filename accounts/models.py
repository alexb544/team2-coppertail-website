from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} Profile"
    

class Dog(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dogs")
    name = models.CharField(max_length=80)
    breed = models.CharField(max_length=80, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.user.username})"
    