from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination

from django_filters import rest_framework as filters

from ...models import Company, Product, Inventory, Registry
from ..serializers import CompanySerializer, ProductSerializer, RegistrySerializer

# V2 API
class CompanyViewSet(ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductViewSet(ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RegistryViewSet(ModelViewSet):
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 