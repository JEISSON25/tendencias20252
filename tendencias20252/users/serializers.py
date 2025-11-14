# users/serializers.py
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser, MovimientoUsuario

# 1. Serializer para CREACIÓN
class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'phone_number')

# 2. Serializer para LECTURA 
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number')
        read_only_fields = ('email',)
        

class MovimientoUsuarioSerializer(serializers.ModelSerializer):

    usuario = serializers.StringRelatedField() 

    class Meta:
        model = MovimientoUsuario
        fields = '__all__'