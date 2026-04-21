from django.db import models
from django.conf import settings         


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    

class Dog(models.Model):
    class Size(models.TextChoices):
        SMALL = "SMALL", "Small"
        MEDIUM = "MEDIUM", "Medium"
        LARGE = "LARGE", "Large"

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dogs")
    name = models.CharField(max_length=80)
    breed = models.CharField(max_length=80, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    size = models.CharField(max_length=10, choices=Size.choices, default=Size.MEDIUM)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"