from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
<<<<<<< HEAD
from .models import Usuario, Rol



class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'



=======
from .models import Usuario


# 🔹 Serializer del modelo Usuario
>>>>>>> upstream/grupo5
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
<<<<<<< HEAD
        extra_kwargs = {
            "password": {"write_only": True}  
        }

   
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado para añadir datos extras al token JWT"""

=======


# 🔹 Serializer personalizado para generar el token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para añadir datos extras al token(JWT)
    """
>>>>>>> upstream/grupo5
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

<<<<<<< HEAD

=======
        # 🔸 Campos que se incluiran en el token
>>>>>>> upstream/grupo5
        token['username'] = user.username
        token['email'] = user.email
        token['telefono'] = user.telefono
        token['rol'] = user.rol.name if user.rol else None

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

<<<<<<< HEAD
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "telefono": self.user.telefono,
            "rol": self.user.rol.name if self.user.rol else None,
        }

        return data
=======
        # 🔹 Estructura del  frontend
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'telefono': self.user.telefono,
            'rol': self.user.rol.name if self.user.rol else None,
        }

        return data
>>>>>>> upstream/grupo5
