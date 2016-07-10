from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import Order, Menu

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'item', 'quantity', 'notes']

ItemFormSet = modelformset_factory(Order, form=OrderForm, extra=2)
