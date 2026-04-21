from django.contrib import admin
from django.urls import path, include # include is needed to reference app urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include("booking.urls")),
    path('services/', include('services.urls')),
<<<<<<< HEAD
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),  # this line connects to the login page(hopefully)
||||||| c99c5d9
=======
    # add about us page here
>>>>>>> 55bf9920c744166e194f4937fd260e379b662eb5
]
