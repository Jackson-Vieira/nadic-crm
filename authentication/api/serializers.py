from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True, 'min_length': 8},
            'passoword': {'required': True, 'write_only':True, 'allow_blank': False, 'min_length': 4},
            'email': {'required': True},
        }
        unique_togueter = [('username', 'email'),]