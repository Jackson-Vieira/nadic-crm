from django.contrib import admin
from django.contrib.admin.options import TabularInline, StackedInline

from .models import Company, Product, Inventory, Registry


# @admin.register(Inventory)
# class ProductModelAdmin(admin.ModelAdmin):
#     inlines = [ProductInline]