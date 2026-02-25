from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from .models import Service

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("service_name", "base_price", "description")
    search_fields = ("service_name", "base_price", "description",)
    list_filter = ("base_price",)
