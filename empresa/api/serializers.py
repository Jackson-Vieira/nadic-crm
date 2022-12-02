from rest_framework import serializers

from ..models import Company, Product, Registry, Inventory

from authentication.serializers import UserSerializer

class CompanySerializer(serializers.ModelSerializer):
    # onwer = UserSerializer()
    class Meta:
        model =  Company
        fields = ('owner','name', 'email', 'total_billing')
        read_only_fields = ('owner',) 
        # pedente extra kwargs (required, readonly fields, ...)

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('product', 'quantity')

class ProductSerializer(serializers.ModelSerializer):
    quantity_in_inventory = serializers.IntegerField(source='inventory.quantity')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'product_type', 'quantity_in_inventory')
        
class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = ('product', 'product_quantity')
        #read_only_fields = ('total_price', 'create_at', 'situation', 'product_price')