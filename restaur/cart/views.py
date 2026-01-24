from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from . import models, forms

# Create your views here.
class CartCreateView(LoginRequiredMixin, CreateView):
    model = models.CartModel
    form = forms.CartForm
    template_name = 'cart/cart_create.html'
    success_url = reverse_lazy('food:foodmodels_list')

    def form_valid(self, form):
        if form.instance.creator == self.request.user:
            return super().form_valid(form)


class CartUpdateView(UpdateView):
    model = models.CartModel
    form = forms.CartForm
    template_name = 'cart/cart_update.html'
    success_url = reverse_lazy('food:foodmodel_list')


class CartDetailView(LoginRequiredMixin, DetailView):
    model = models.CartModel
    template_name = 'cart/cart_details.html'
    context_object_name = 'cart_details'


class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = models.CartModel
    template_name = 'cart/cart_delete.html'
    success_url = reverse_lazy('food:foodmodel_list')


