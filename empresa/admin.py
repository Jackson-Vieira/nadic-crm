from django.contrib import admin
from django.contrib.admin.options import TabularInline, StackedInline

from .models import Company, Product, Inventory, Registry

@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'total_billing']
    fields = ['name', 'owner', 'total_billing']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Inventory)
class InventoryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Registry)
class RegistryModelAdmin(admin.ModelAdmin):
    pass