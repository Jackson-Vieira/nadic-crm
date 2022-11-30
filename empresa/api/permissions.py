from rest_framework import permissions
from .utils.validators import user_has_company

class HasCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_company(request.user)

# class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.mehtod == permissions.SAFE_METHODS:
#             pass
#         return obj.owner == request.user