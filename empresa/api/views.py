from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from ..models import Company, Product, Inventory, Registry
from .serializers import CompanySerializer, ProductSerializer, InventorySerializer, RegistrySerializer

# class CompanyViewSet(ModelViewSet):
#     model = Company
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer

# class ProductViewSet(ModelViewSet):
#     model = Product
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class InventoryViewSet(ModelViewSet):
#     model = Inventory
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer 

# class RegistryViewSet(ModelViewSet):
#     model = Registry
#     queryset = Registry.objects.all()
#     serializer_class = RegistrySerializer 


# COMPANY VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_company(request):
    data = request.data
    data['owner'] = request.user.id
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_company_stats(request):
    user = request.user

    # user without a company validation
    company = user.company
    serializer = CompanySerializer(user.company)
    return Response(serializer.data)


api_view(['GET'])
def get_current_user_company_products(request):
    user = request.user
    # user company without products
    products = user.company.products
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


api_view(['GET'])
def get_current_user_company_registrys(request):
    user = request.user
    # user company without registrys
    registrys = user.company.registrys
    serializer = RegistrySerializer(registrys, many=True)
    return Response(serializer.data)


# PRODUCTS VIEWS
@api_view(['POST'])
def new_product(request):
    pass

api_view(['GET'])
def get_product_detail(request, product_id):
    pass

api_view(['PUT'])
def edit_product(request, registry_id):
    pass

api_view(['DELETE'])
def delete_product(request, product_id):
    pass

# INVENTORY VIEWS
api_view(['POST'])
def new_inventory(request):
    pass

api_view(['PUT'])
def edit_inventory(request):
    pass

#  REGISTRYS VIEWS
api_view(['POST'])
def new_registry(request):
    pass

api_view(['GET'])
def get_registry_detail(request, registry_id):
    pass