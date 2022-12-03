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
from ..serializers import CompanySerializer, ProductSerializer, RegistrySerializer, InventorySerializer
from .filters import *
from ..permissions import IsOwner, IsOwnerOrReadOnly, HasCompanyOrReadOnly
from ..utils.validators import user_has_company

class CompanyViewSet(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not user_has_company(request.user):
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'there is already a company linked to this user'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsOwner])
    def stats(self, request, pk = None):
        company = self.get_object()
        return Response(
            {
            'stats': {
                'total_billing': company.total_billing,
                }
            },
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, HasCompanyOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=request.user.company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['GET'], serializer_class=InventorySerializer)
    def inventory(self, request, pk = None):
        product = self.get_object()
        inventory = product.inventory
        serializer = self.get_serializer(instance=inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @inventory.mapping.put
    def update_inventory(self, request, pk = None):
        product = self.get_object()
        inventory = product.inventory
        serializer = InventorySerializer(instance=inventory, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistryViewSet(viewsets.ModelViewSet):
    # only post and get methods
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, HasCompanyOrReadOnly, IsOwner]
    # ListModelMixin, 
    # CreateModelMixin
    # RetrieveModelMixin -  Only visible for the owner of the empresa

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=request.user.company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)