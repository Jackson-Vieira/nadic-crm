from django.contrib import admin

from .models import Company, Product, Order, Inventory, Sale

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Sale)