from rest_framework.response import Response
from rest_framework import status

from ...models import Company

def user_has_company(user, exception_error=False):
    return  Company.objects.filter(owner=user).exists()