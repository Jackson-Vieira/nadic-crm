from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from django.shortcuts import get_object_or_404

from ..models import Company, Product, Inventory, Registry
from .serializers import CompanySerializer, ProductSerializer, InventorySerializer, RegistrySerializer

# COMPANY VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_company(request):
    # Verificar se o usuario já tem uma empresa
    data = request.data
    serializer = CompanySerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(owner=request.user)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_company_stats(request):
    user = request.user
    # user without a company validation
    company = user.company
    serializer = CompanySerializer(user.company)
    return Response(serializer.data)

@api_view(['GET'])
def get_current_user_company_products(request):
    user = request.user
    products = Product.objects.filter(company=user.company)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_current_user_company_registrys(request):
    user = request.user
    registrys = Registry.objects.filter(company=user.company)
    serializer = RegistrySerializer(registrys, many=True)
    return Response(serializer.data)

# PRODUCTS VIEWS
@api_view(['POST'])
def new_product(request):
    company = Company.objects.get(owner=request.user)
    data = request.data
    data['company'] = company.id
    serializer = ProductSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        product = serializer.save()
        Inventory.objects.create(product=product)
        return Response(serializer.data)

@api_view(['GET'])
# autenticação, permissão
def get_product_detail(request, product_id):
    user = request.user
    company_products = Product.objects.filter(company=user.company)
    product =  get_object_or_404(company_products, pk=product_id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
    
@api_view(['POST'])
# autenticação, permissão
def edit_product(request, product_id):
    user = request.user
    company_products = Product.objects.filter(company=user.company)
    product =  get_object_or_404(company_products, pk=product_id)
    data = request.data
    serializer = ProductSerializer(instance=product, data=data, many=False)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    # return Response(serializer.errors)

@api_view(['GET'])
# autenticação, permissão
def delete_product(request, product_id):
    product =  get_object_or_404(Product, pk=product_id)
    product.delete()

    response = {
        'message': 'product has been permanently deleted'
    }

    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
# autenticação, permissão
def get_inventory_detail(request, product_id):
    user = request.user
    company_products = Product.objects.filter(company=user.company)
    product =  get_object_or_404(company_products, pk=product_id)
    inventory = Inventory.objects.get(product=product)
    serializer = InventorySerializer(inventory, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def edit_inventory(request, product_id):
    user = request.user
    company_products = Product.objects.filter(company=user.company)
    product =  get_object_or_404(company_products, pk=product_id)
    inventory = Inventory.objects.get(product=product)
    data = request.data
    serializer = InventorySerializer(instance=inventory, data=data, many=False)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

#  REGISTRYS VIEWS
@api_view(['POST'])
def new_registry(request):
    # validação 
    # permitir registros de produtos disponíveis da empresa
    # definir a situação do registro depedendo da quantidade solicitada
    company = Company.objects.get(owner=request.user)
    data = request.data
    data['company'] = company.pk
    serializer = RegistrySerializer(request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
def get_registry_detail(request, registry_id):
    registry =  get_object_or_404(Registry, pk=registry_id)
    serializer = ProductSerializer(registry, many=False)
    return Response(serializer.data)