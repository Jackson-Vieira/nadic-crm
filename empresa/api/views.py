from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404

from ..models import Company, Product, Inventory, Registry, RegistrySituation
from .serializers import CompanySerializer, ProductSerializer, InventorySerializer, RegistrySerializer
from .utils.validators import user_has_company
from .permissions import HasCompany

# COMPANY VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_company(request):
    user = request.user
    if not user_has_company(user):
        data = request.data
        serializer = CompanySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': 'there is already a company linked to this user'})

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_current_user_company(request):
    user = request.user
    serializer = CompanySerializer(user.company)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_current_user_company_stats(request):
    user = request.user
    serializer = CompanySerializer(user.company)

    # querys 
    response = {}
    
    return Response(serializer.data)
   
@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_current_user_company_products(request):
    user = request.user
    products = Product.objects.filter(company=user.company)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
   
@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_current_user_company_registrys(request):
    user = request.user
    registrys = Registry.objects.filter(company=user.company)
    serializer = RegistrySerializer(registrys, many=True)
    return Response(serializer.data)
    
# PRODUCTS VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated, HasCompany])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        product = serializer.save(company=request.user.company)
        Inventory.objects.create(product=product)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_product_detail(request, product_id):
    user = request.user
    product =  get_object_or_404(Product, pk=product_id)
    if product.company == user.company:
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    return Response({'message': 'you do not have permission access for this resource'},status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated, HasCompany])
def edit_product(request, product_id):
    user = request.user
    product =  get_object_or_404(Product, pk=product_id)

    if product.company == user.company:
        data = request.data
        serializer = ProductSerializer(instance=product, data=data, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response({'message': 'you do not have permission to edit this resource'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def delete_product(request, product_id):
    user = request.user

    product =  get_object_or_404(Product, pk=product_id)
    if product.company == user.company:
        product.delete()
        response = {
        'message': 'product has been permanently deleted'
    }
        return Response(response, status=status.HTTP_200_OK)

    return Response({'message': 'you do not have permission to delete this resource'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_inventory_detail(request, product_id):
    user = request.user
    product =  get_object_or_404(Product, pk=product_id)

    if product.company == user.company:
        inventory = Inventory.objects.get(product=product)
        serializer = InventorySerializer(inventory, many=False)
        return Response(serializer.data)
    return Response({'message': 'you do not have permission access this resource'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated, HasCompany])
def edit_inventory(request, product_id):
    user = request.user

    product =  get_object_or_404(Product, pk=product_id)

    if product.company == user.company:
        inventory = Inventory.objects.get(product=product)
        data = request.data
        serializer = InventorySerializer(instance=inventory, data=data, many=False)
        if serializer.is_valid(raise_exception=True):

            # não permitir diminuir o estoque para valores negativos

            serializer.save()
            return Response(serializer.data)
        
    return Response({'message': 'you do not have permission to edit this resource'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated, HasCompany])
def new_registry(request):
    user = request.user
    data = request.data
    serializer = RegistrySerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        product = Product.objects.get(pk=data.get('product'))
        registry = serializer.save(company=user.company, product_price=product.price)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasCompany])
def get_registry_detail(request, registry_id):
    user = request.user
    registry =  get_object_or_404(Registry, pk=registry_id)

    if registry.company == user.company:
        serializer = ProductSerializer(registry, many=False)
        return Response(serializer.data)

    return Response({'message': 'you do not have permission to acess this resource'}, status=status.HTTP_401_UNAUTHORIZED) 