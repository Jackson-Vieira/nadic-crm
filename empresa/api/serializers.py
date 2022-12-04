from rest_framework import serializers

from ..models import Company, Product, Registry, Inventory

from authentication.api.serializers import UserSerializer

class CompanySerializer(serializers.ModelSerializer):
    
    # onwer = UserSerializer()
    class Meta:
        model =  Company
        fields = ('name', 'email')
    
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('quantity',)
        
class ProductSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'company', 'name', 'description', 'price', 'product_type', 'inventory')
        read_only_fields = ('company',)

class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = ('id', 'product', 'product_quantity', 'total_price','situation', 'product_price', 'created_at')
        read_only_fields = ('total_price','situation', 'product_price', 'create_at')