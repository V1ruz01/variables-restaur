from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from . import models, forms

# Create your views here.
class CartUpdateView(UpdateView):
    model = models.CartModel
    form = forms.CartForm
    template_name = 'cart/cart_update.html'
    success_url = reverse_lazy('cart:cart_update')


class CartDetailView(LoginRequiredMixin, DetailView):
    model = models.CartModel
    template_name = 'cart/cart_details.html'
    context_object_name = 'cart_det'

    def get_object(self):
        return self.request.user.cart_det

class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = models.CartModel
    template_name = 'cart/cart_delete.html'
    success_url = reverse_lazy('cart:cart_delete')


