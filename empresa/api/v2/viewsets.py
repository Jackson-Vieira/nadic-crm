from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, 
    CreateModelMixin, 
    DestroyModelMixin, 
    UpdateModelMixin, 
    RetrieveModelMixin
    )

from django_filters import rest_framework as filters

from ...models import Company, Product, Inventory, Registry
from ..serializers import CompanySerializer, ProductSerializer, RegistrySerializer
from .filters import *
# V2 API
class CompanyViewSet(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # action inventory - GET, PUT

class RegistryViewSet(viewsets.ModelViewSet):
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 