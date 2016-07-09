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
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemFormSet(self.request.POST)
        else:
            context['formset'] = ItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            forset.server = self.request.user
            formset.save()
            return redirect ("index_view")
        else:
            return self.render_to_response(self.get_context_data(form=form))
