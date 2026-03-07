from django.db import models
from food.models import FoodModel
from django.contrib.auth.models import User

# Create your models here.
class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    in_cart_productes = models.ManyToManyField(FoodModel, blank=True)
    title = models.CharField(max_length=4, default='Cart')
    desc = models.CharField(max_length=1000, blank=True)


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.user.username}'s cart"
