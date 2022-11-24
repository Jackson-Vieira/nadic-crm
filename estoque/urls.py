from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.home, name='home'),
    path('empresa/', views.empresa, name='empresas'), 
    path('empresa/estoques/', views.estoques, name='estoques'), 
    path('empresa/estoques/<str:pk>/', views.estoque, name='estoque_info'), 
    path('empresa/estoques/<str:pk_estoque>/products/<str:pk_product>', views.product, name='product'), 

    path('empresa/new', views.new_empresa, name='new_empresa'), 
    path('empresa/products/new', views.new_product, name='new_product'), 
    path('empresa/estoques/new', views.new_estoque, name='new_estoque'), 
    path('empresa/sales/new', views.new_sale, name='new_sale'), 
    ]