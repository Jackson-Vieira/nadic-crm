from rest_framework import status

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view


from ..models import Company, Product, Inventory, Registry
from .serializers import CompanySerializer, ProductSerializer, InventorySerializer, RegistrySerializer

class CompanyViewSet(ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductViewSet(ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryViewSet(ModelViewSet):
    model = Inventory
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer 

class RegistryViewSet(ModelViewSet):
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 

