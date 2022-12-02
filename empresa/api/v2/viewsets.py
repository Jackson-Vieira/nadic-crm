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
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from django_filters import rest_framework as filters

from ...models import Company, Product, Inventory, Registry
from ..serializers import CompanySerializer, ProductSerializer, RegistrySerializer
from .filters import *
from ..utils.validators import user_has_company

# V2 API
class CompanyViewSet(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not user_has_company(request.user):
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': 'there is already a company linked to this user'}) # change status

    # stats -> action - apenas o dono da empresa
    # retrieve
    # products
    # registrys

class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        pass
    # action inventory - GET, PUT

class RegistryViewSet(viewsets.ModelViewSet):
     # only post and get methods
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 

   