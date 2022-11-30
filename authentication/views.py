from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_detail(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
