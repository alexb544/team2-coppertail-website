from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from .models import Profile, Dog

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


class DogInline(admin.TabularInline):
    model = Dog
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(attrs={"rows": 2, "style": "width: 95%"})
        }
    }


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "address")
    search_fields = (
        "user__username", 
        "user__first_name", 
        "user__last_name", 
        "user__email",
        "phone_number",
        "address",
    )
    inlines = [DogInline]


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "breed", "age")
    search_fields = (
        "name",
        "breed", 
        "owner__user__first_name",
        "owner__user__last_name",
    )
    list_filter = ("breed",)