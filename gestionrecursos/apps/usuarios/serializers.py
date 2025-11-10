from rest_framework import serializers
from .models import Usuarios
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = "__all__"
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'rol', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuarios(**validated_data)
        user.set_password(password)
        user.save()
        return user