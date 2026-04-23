from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include # include is needed to reference app urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include("booking.urls")),
    path('services/', include('services.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),  # keep this below named routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
