from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from app.models import Profile, Order, Menu
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import ItemFormSet, OrderForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

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

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.user
        return super().form_valid(form)

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
    template_name = 'app/order_form.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('profile_update_view')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        print(form_class)
        form = self.get_form(form_class)
        item_form = ItemFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, item_form=item_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormSet(self.request.POST)
        if (form.is_valid() and item_form.is_valid()):
            print('valid')
            return self.form_valid(form, item_form)
        else:
            print('invalid')
            return self.form_invalid(form, item_form)

    def form_valid(self, form, item_form):
        self.object = form.save(commit=False)
        item_form.instance = self.object
        item_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, item_form):
        return self.render_to_response(
            self.get_context_data(form=form, item_form=item_form))
