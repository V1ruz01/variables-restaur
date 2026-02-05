from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

app_name = 'account'

urlpatterns = [
    path('', MenuView.as_view(), name='main_menu'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='register/logout.html'), name='logout'),
]
