from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import FoodForm
# Create your views here.


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = FoodModel
    form_class = FoodForm
    template_name = 'food/create_food.html'
    success_url = reverse_lazy('food:foodmodels_list')

    def form_valid(self, form):
        if form.instance.creator == self.request.user:
            return super().form_valid(form)


class FoodUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodModel
    form_class = FoodForm
    template_name = 'food/update_food.html'
    success_url = reverse_lazy('food:foodmodel_list')


class FoodDetailView(DetailView):
    model = FoodModel
    template_name = 'food/detail_food.html'
    context_object_name = 'food_details'


class FoodDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodModel
    template_name = 'food/delete_food.html'
    success_url = reverse_lazy('food:foodmodel_list')


