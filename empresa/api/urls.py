from . import views

from django.urls import path

urlpatterns = []

# V1 API
urls_v1 = [
    path('companys/', views.new_company, name='new_company' ),
    path('me/company/', views.get_current_user_company_stats, name='current_user_company'),

    path('me/company/products/', views.get_current_user_company_products, name='current_user_company_products'),
    path('me/company/products/new/', views.new_product, name='current_user_company_new_product'),
    path('me/company/products/<int:product_id>/', views.get_product_detail, name='detail_product'),
    path('me/company/products/<int:product_id>/edit/', views.edit_product, name='edit_detail'),
    path('me/company/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    path('me/company/registrys/', views.get_current_user_company_registrys, name='current_user_company_registrys'),
    path('me/company/registrys/new/', views.new_registry, name='current_user_company_new_registry'),
    path('me/company/registrys/<int:registry_id>/', views.get_registry_detail, name='detail_registry'),

    path('me/company/products/<int:product_id>/inventory/', views.get_inventory_detail, name='detail_inventory'),
    path('me/company/products/<int:product_id>/inventory/edit/', views.edit_inventory, name='edit_inventory'),
]

urlpatterns += urls_v1