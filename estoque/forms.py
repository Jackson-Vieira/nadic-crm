from django import forms

from .models import Empresa, Product, Inventory, Order
from django.forms import inlineformset_factory


class EmpresaModelForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['name', 'email', 'type']

class ProdutModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'tipo', 'fabricatedAt']
    
class EstoqueModelForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity', 'product']

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        