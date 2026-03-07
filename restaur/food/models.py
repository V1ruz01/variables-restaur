from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodModel(models.Model):
    class FoodType(models.TextChoices):
        FRUIT = 'Fruit',
        VEGET = 'Vetetable',
        DRINK = 'Drink'


    food_name = models.CharField(max_length=60, unique=True)
    desc = models.CharField(blank=True, max_length=5000, null=True, default='No Description Provided')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='food')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Food'


    def __str__(self):
        self.food_name

