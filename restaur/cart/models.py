from django.db import models
from food.models import FoodModel
from django.contrib.auth.models import User

# Create your models here.
class CartModel(models.Model):
    in_cart_productes = models.ManyToManyField(FoodModel, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    title = models.CharField(max_length=4, default='Cart')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'