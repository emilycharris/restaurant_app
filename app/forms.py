from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Order, Menu

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'quantity', 'notes']

class ItemForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['item']


ItemFormSet = inlineformset_factory(Menu, Order, form=OrderForm)
