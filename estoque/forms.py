from django import forms

from .models import Empresa, Product, Inventory, Order, Sale
from django.forms import inlineformset_factory

class EmpresaModelForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['name', 'email']


class ProdutModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'tipo', 'fabricatedAt']

class EstoqueModelForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['empresa', 'quantity', 'product']

SaleFormSet = inlineformset_factory(Sale, Order, fields=('product', 'quantity'))