from django import forms
from . import models

class CartForm(forms.ModelForm):
    class Meta:
        model = models.CartModel
        exclude = ["creator"]
