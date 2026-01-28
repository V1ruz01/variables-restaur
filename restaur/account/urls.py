from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='templates/register'), name='login'),
]
