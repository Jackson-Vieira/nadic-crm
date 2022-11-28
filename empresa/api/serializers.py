
from rest_framework import serializers

from ..models import Company, Product, Registry, Inventory


class CompanySerializer(serializers.ModelSerializer):
    # onwer = UserSerializer()
    class Meta:
        model =  Company
        fields = ('owner','name', 'email', 'total_billing')
        # pedente extra kwargs (required, readonly fields, ...)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('company', 'name', 'description', 'price', 'product_type')

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('product', 'quantity')

class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = ('product', 'product_quantity', 'product_price','create_at',  'situation')
        read_only_fields = ('total_price')