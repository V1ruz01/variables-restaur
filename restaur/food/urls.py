from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *

app_name = 'food'

urlpatterns = [
    path('', FoodMenuView.as_view(), name='main_menu'),
    path('create/', FoodCreateView.as_view(), name='food_create'),
    path('<int:pk>/', FoodDetailView.as_view(), name='food_details'),
    path('update<int:pk>/', FoodUpdateView.as_view(), name='food_update'),
    path('delete/<int:pk>/', FoodDeleteView.as_view(), name='food_detele'),
    path('login/', LoginView.as_view(template_name='register/login.html'), name='login'),
]
