from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ...models import Company, Product, Inventory, Registry
from ..serializers import CompanySerializer, ProductSerializer, RegistrySerializer, InventorySerializer
from .filters import *
from ..permissions import IsOwner, IsOwnerOrReadOnly, HasCompanyOrReadOnly
from ..utils.validators import user_has_company
from .pagination import CustomPageNumberPagination, CustomLimitOffsetPagination

from django.db.models import Sum, Avg, Count, Min, Max, F
from django.shortcuts import get_object_or_404

class CompanyViewSet(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]
    pagination_class = CustomPageNumberPagination

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

        # QUERIES
        stats = Company.objects.filter(pk=pk).prefetch_related(
                'registrys', 'products', 'products__inventory'
                ) \
            .annotate(
                max_registry_price = Max('registrys__product_price'),
                avg_product_price = Avg('products__price'),
                min_product_quantity = Min('products__inventory__quantity'),
            ).values('max_registry_price', 'min_product_quantity', 'total_billing', 'avg_product_price')[0]

        return Response(
                stats
            ,
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, HasCompanyOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilterSet

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

class RegistryViewSet(
    # only post and get methods allowed
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
   
    model = Registry
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, HasCompanyOrReadOnly]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RegistrysFilterSet

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=request.data.get('product'))
        serializer.save(company=request.user.company, product_price=product.price)
        return Response(serializer.data, status=status.HTTP_201_CREATED)