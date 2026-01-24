from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('create/', views.CartCreateView.as_view(), name='cart_create'),
    path('update/<int:pk>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('<int:pk>', views.CartDetailView.as_view(), name='cart_detail'),
]