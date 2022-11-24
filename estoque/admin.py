from django.contrib import admin
from django.contrib.admin.options import TabularInline

from .models import Empresa, Product, Order, Inventory, Sale

class OrderInline(TabularInline):
    extra = 1
    model = Order
    readonly_fields = ['situation', 'createdAt']

@admin.register(Empresa)
class EmpresaModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'faturamento_total']
    readonly_fields = ['faturamento_total']
    search_fields = ['name', 'owner']

@admin.register(Sale)
class SaleModelAdmin(admin.ModelAdmin):
    inlines = (OrderInline, )
    list_display = ['id', 'empresa']
    search_fields = ['empresa', ]
    list_filter = ['boughtAt',]

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'inventory']
    readonly_fields = []
    search_fields = ['name']
    list_filter = ['tipo',]

@admin.register(Inventory)
class ProductManagerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'empresa', 'quantity']
    list_filter = ['empresa',]