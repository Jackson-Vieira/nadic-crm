
from . import views

from django.urls import path

urlpatterns = [
    path('companys/', views.new_company, name='new_company' ),
    path('me/company/', views.get_current_user_company_stats, name='current_user_company'),
    path('me/company/products/', views.get_current_user_company_products, name='current_user_company_products'),
    path('me/company/products/<int:product_id>/', views.get_product_detail, name='product_detail'),
    path('me/company/registrys/', views.get_current_user_company_registrys, name='current_user_company_registrys'),
    path('me/company/registrys/<int:registry_id>/', views.get_registry_detail, name='registry_detail'),
]