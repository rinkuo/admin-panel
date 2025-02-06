from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_id', 'order_date', 'status', 'customer_name', 'customer_email', 'customer_phone', 'customer_address']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_id'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['order_date'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['status'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['customer_name'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['customer_email'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['customer_phone'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})
        self.fields['customer_address'].widget.attrs.update({'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm'})

OrderItemFormSet = modelformset_factory(OrderItem, fields=('product', 'quantity', 'price'), extra=1)

from django import forms
from .models import OrderItem
from products.models import Product

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)


