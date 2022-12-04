from django_filters import rest_framework as filters

from ...models import Product, Registry

class ProductFilterSet(filters.FilterSet):
    keyword = filters.CharFilter(field_name='name', lookup_expr='icontains')
    company = filters.CharFilter(field_name='company__name', lookup_expr='exact')

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['company', 'keyword', 'product_type', 'max_price', 'min_price']


class RegistrysFilterSet(filters.FilterSet):

    company = filters.CharFilter(field_name='company__name', lookup_expr='exact')

    min_product_quantity =  filters.NumberFilter(field_name='product_quantity', lookup_expr='gte')
    max_product_quantity = filters.NumberFilter(field_name='product_quantity', lookup_expr='lte')

    class Meta:
        model = Registry
        fields = ['company', 'product', 'situation', 'min_product_quantity', 'max_product_quantity']