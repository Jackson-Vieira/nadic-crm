from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.home, name='home'),
    path('empresa/', views.empresa, name='empresa'), 
    path('empresa/registros/', views.registros, name='registros'), 
    path('empresa/estoques/', views.estoques, name='estoques'), 
    path('empresa/estoques/<str:pk>/', views.estoque, name='estoque_info'), 
    path('empresa/estoques/<str:pk_estoque>/products/<str:pk_product>', views.product, name='product'), 

    path('empresa/new', views.new_empresa, name='new_empresa'), 
    path('empresa/estoques/new', views.new_estoque, name='new_estoque'), 
    path('empresa/estoques/<int:pk>/delete', views.delete_estoque, name='delete_estoque'), 
    path('empresa/estoques/<int:pk>/edit', views.edit_estoque, name='edit_estoque'), 
    path('empresa/registros/new', views.new_registro, name='new_registro'), 
    ]