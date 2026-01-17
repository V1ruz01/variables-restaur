from django import forms
from .models import FoodModel

class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodModel
        fields = ('food_name', 'desc')