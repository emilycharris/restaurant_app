from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.models import User
from app.models import Profile, Order, Menu
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy




# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login"

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['position']
    success_url = reverse_lazy('index_view') #change reverse_lazy

    def get_object(self, queryset=None):
        return self.request.user.profile

class CreateMenuItemView(CreateView):
    model = Menu
    fields = ['item', 'description', 'category', 'price', 'photo']
    success_url = reverse_lazy('profile_update_view')

class UpdateMenuItemView(UpdateView):
    model = Menu
    fields = ['item', 'description', 'category', 'price', 'photo']
    success_url = reverse_lazy('profile_update_view')

    def get_queryset(self, **kwargs):
        item_id = self.kwargs.get('pk')
        return Menu.objects.filter(id=item_id)
