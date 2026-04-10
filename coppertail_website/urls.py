from django.contrib import admin
from django.urls import path, include # include is needed to reference app urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include("booking.urls")),
    path('services/', include('services.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),  # this line connects to the login page(hopefully)
]
