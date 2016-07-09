from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
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
    success_url = reverse_lazy('profile_update_view')

    def get_object(self, queryset=None):
        return self.request.user.profile

class MenuItemCreateView(CreateView):
    model = Menu
    fields = ['item', 'description', 'category', 'price', 'photo']
    success_url = reverse_lazy('profile_update_view')

class MenuItemListView(ListView):
    model = Menu
    template_name = 'app/menu_list.html'

    def get_queryset(self):
        return Menu.objects.all().order_by('category')


class MenuItemDetailView(DetailView):
    model = Menu

    def get_queryset(self, **kwargs):
        item_id = self.kwargs.get('pk')
        return Menu.objects.filter(id=item_id)


class MenuItemUpdateView(UpdateView):
    model = Menu
    fields = ['item', 'description', 'category', 'price', 'photo']
    success_url = reverse_lazy('profile_update_view')

    def get_queryset(self, **kwargs):
        item_id = self.kwargs.get('pk')
        return Menu.objects.filter(id=item_id)

class MenuItemDeleteView(DeleteView):
    success_url = reverse_lazy("menu_item_list_view")
    def get_queryset(self):
        return Menu.objects.all()


class OrderCreateView(CreateView):
    model = Order
    fields = ['guest_number', 'item', 'quantity', 'notes']
    success_url = reverse_lazy('index_view')
