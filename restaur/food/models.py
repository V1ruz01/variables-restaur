from django.db import models

# Create your models here.
class FoodModel(models.Model):
    class FoodType(models.TextChoices):
        FRUIT = 'Fruit',
        VEGET = 'Vetetable',
        DRINK = 'Drink'


    food_name = models.CharField(max_length=60, unique=True)
    desc = models.CharField(blank=True, max_length=5000, null=True, default='No Description Provided')

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Food'


    def __str__(self):
        self.food_name

