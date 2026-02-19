from django.urls import path
from . import views

# App namespace (for URL reversing)
app_name = 'accounts'

urlpatterns = {
        path('', views.accounts, name='accounts'),
}
