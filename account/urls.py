from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('account/register', RegisterView.as_view(), name="sign_up"),
]