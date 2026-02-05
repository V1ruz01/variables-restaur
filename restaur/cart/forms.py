from django import forms
from . import models

class CartForm(forms.Form):
    model = models.FoodModel
    class Meta:
        fields = {'title'}
