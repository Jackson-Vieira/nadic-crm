from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('empresa/new', views.new_empresa, name='new_empresa'), 
    ]