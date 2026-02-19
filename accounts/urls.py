from django.urls import path
<<<<<<< userloginpage
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
]
=======
from . import views

# App namespace (for URL reversing)
app_name = 'accounts'

urlpatterns = {
        path('', views.accounts, name='accounts'),
}
>>>>>>> development
