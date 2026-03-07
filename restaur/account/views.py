from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import CreateView, ListView
from django.shortcuts import redirect

from food.models import FoodModel


# Create your views here.
class RegisterView(CreateView):
    template_name = 'register/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('account:login')

    def is_form_valid(self, form):
        responce = super().form_valid(self)
        login(self.request, self.object)
        return responce

class MenuView(ListView):
    model = FoodModel
    template_name = 'food/foodmodel_list.html'
    context_object_name = 'main_menu'