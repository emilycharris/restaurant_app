from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from app.models import Profile, Order, Menu, Items
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet

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

class ListItemCreateView(CreateView):
        pass

class ItemInlineView(InlineFormSet):
    model = Items
    fields = ['item', 'quantity', 'notes']


class OrderCreateView(CreateWithInlinesView):
    model = Order
    inlines = [ItemInlineView]
    fields = ['paid', 'fulfilled']
    extra = 3

    def forms_valid(self, form, inlines):
        form = form.save(commit=False)
        form.server = self.request.user
        form.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(reverse_lazy('profile_update_view'))

#django-extra-views https://github.com/AndrewIngram/django-extra-views/


class OrderListView(ListView):
    model = Order
    template_name = 'app/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(fulfilled=False).order_by('-created')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['items'] = Items.objects.all()
    #     return context



class OrderDetailView(ListView):
    model = Items
    template_name = 'app/order_detail.html'

    def get_queryset(self, **kwargs):
        order_id = self.kwargs.get('pk')
        print(order_id)
        print(Items.objects.filter(order_id=order_id))
        return Items.objects.filter(order_id=order_id)
