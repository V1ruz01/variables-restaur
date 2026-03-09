from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from django.views import View
from food.models import FoodModel
from cart.models import CartModel
from . import models, forms

# Create your views here.
class CartUpdateView(UpdateView):
    model = models.CartModel
    form = forms.CartForm
    template_name = 'cart/cart_update.html'
    success_url = reverse_lazy('cart:cart_update')


class CartDetailView(LoginRequiredMixin, DetailView):
    model = CartModel
    template_name = 'cart/cart_details.html'
    context_object_name = 'cart'

    def get_object(self):
        cart, _ = CartModel.objects.get_or_create(user=self.request.user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object()
        items = cart.in_cart_productes.all()
        context['cart_items'] = items
        total = 0
        # prevent crash
        for f in items:
            try:
                total += float(f.price) if f.price else 0 
            except (ValueError, TypeError):
                pass
        context['total_price'] = total
        return context
    

class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = models.CartModel
    template_name = 'cart/cart_delete.html'
    success_url = reverse_lazy('cart:cart_delete')

#ОСТОРОЖНО! Два Инвалида
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        food = get_object_or_404(FoodModel, pk=pk)
        cart, _ = CartModel.objects.get_or_create(user=request.user)
        cart.in_cart_productes.add(food)
        cart.save()
        return redirect('cart:cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        food = get_object_or_404(FoodModel, pk=pk)
        cart, _ = CartModel.objects.get_or_create(user=request.user)
        cart.in_cart_productes.remove(food)
        return redirect('cart:cart_detail')

