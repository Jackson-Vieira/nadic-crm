from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer

from django.shortcuts import render

from django.contrib.auth.models import User


@api_view(['POST'])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data=data)
    username= data.get('email')
    if not User.objects.filter(username=username).exists():
        if serializer.is_valid():
            password = data.get('password')
            serializer.save(username=username, password=make_password(password))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'A User with the this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_detail(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
