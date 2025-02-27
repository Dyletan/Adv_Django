from django import forms
from .models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'products', 'discount_percent', 'notes'] # Include fields for sales order creation