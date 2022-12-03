from rest_framework import permissions
from .utils.validators import user_has_company

from ..models import Product, Company, Inventory

def check_permission(obj, request):
    user = request.user
    if type(obj) == Product:
        return obj.company ==  user.company
    if type(obj) == Inventory:
        return obj.product.company == user.company
    if type(obj) == Company:
        return obj.owner == user

class HasCompanyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_has_company(request.user)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return check_permission(obj, request)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_permission(obj, request)