from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('update/<int:pk>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('', views.CartDetailView.as_view(), name='cart_detail'),
]