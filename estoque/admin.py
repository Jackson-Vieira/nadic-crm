from django.contrib import admin
from django.contrib.admin.options import TabularInline, StackedInline

from .models import Empresa, Product, Order, Inventory, Sale

class OrderInline(TabularInline):
    extra = 1
    model = Order

class ProductInline(StackedInline):
    model = Product
    extra = 1

@admin.register(Empresa)
class EmpresaModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleModelAdmin(admin.ModelAdmin):
    inlines = (OrderInline, )

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Inventory)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductInline]