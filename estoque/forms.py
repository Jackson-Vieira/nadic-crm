from django import forms

from .models import Empresa, Product, Inventory, Order

class EmpresaModelForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['name', 'email']