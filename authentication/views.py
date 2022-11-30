from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer

from django.shortcuts import render

@api_view(['POST'])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        username= data.get('username')
        password = data.get('password')
        serializer.save(username=username, password=make_password(password))
        return Response(serializer.data)
    return Response(serializer.errors)