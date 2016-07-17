from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from app.models import Profile, Order, Menu, Items, Category
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet
from decimal import *

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
    success_url = reverse_lazy('menu_item_list_view')

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.user
        return super().form_valid(form)

class MenuItemListView(ListView):
    model = Category
    template_name = 'app/menu_list.html'

    def get_queryset(self):
        category = Category.objects.all()
        return category


class MenuItemDetailView(DetailView):
    model = Menu

    def get_queryset(self, **kwargs):
        item_id = self.kwargs.get('pk')
        return Menu.objects.filter(id=item_id)


class MenuItemUpdateView(UpdateView):
    model = Menu
    fields = ['item', 'description', 'category', 'price', 'photo']
    success_url = reverse_lazy('menu_item_list_view')

    def get_queryset(self, **kwargs):
        item_id = self.kwargs.get('pk')
        return Menu.objects.filter(id=item_id)

class MenuItemDeleteView(DeleteView):
    success_url = reverse_lazy("menu_item_list_view")

    def get_queryset(self):
        return Menu.objects.all()

class ListItemCreateView(CreateView):
        pass

class ItemInlineView(InlineFormSet):
    model = Items
    fields = ['item', 'quantity', 'notes']


class OrderCreateView(CreateWithInlinesView):
    model = Order
    inlines = [ItemInlineView]
    fields = ['paid', 'fulfilled']

    def forms_valid(self, form, inlines):
        form = form.save(commit=False)
        form.server = self.request.user
        form.save()
        for formset in inlines:
            print(formset.instance)
            formset.save()
        return HttpResponseRedirect(reverse_lazy('profile_update_view'))

#django-extra-views https://github.com/AndrewIngram/django-extra-views/


class OrderListView(ListView):
    model = Order
    template_name = 'app/order_list.html'

    def get_queryset(self):
        if self.request.user.profile.position.id == 2:
            return Order.objects.filter(fulfilled=False).order_by('created')
        if self.request.user.profile.position.id == 1:
            return Order.objects.filter(paid=False).order_by('created')


class OrderUpdateView(UpdateWithInlinesView):
    model = Order
    fields = ['paid', 'fulfilled']
    template_name = 'app/order_update.html'
    success_url = reverse_lazy('order_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['order'] = Order.objects.get(id=pk)
        items = Items.objects.filter(order_id=pk)

        tax_rate = 0.08
        tax_rate_for_total = 1.08
        subtotal = 0
        tax_total = 0
        grand_total = 0


        for item in items:
            subtotal += (item.item.price * item.quantity)
            item_tax = round(Decimal(item.item.price * item.quantity) * Decimal(tax_rate),2)
            tax_total += item_tax
            item_total = round(Decimal(item.item.price * item.quantity) + Decimal(item_tax),2)
            grand_total += item_total

        context['items'] = items
        context['tax_rate'] = tax_rate
        context['tax_total'] = tax_total
        context['tax_rate_for_total'] = tax_rate_for_total
        context['subtotal'] = subtotal
        context['grand_total'] = grand_total
        return context
