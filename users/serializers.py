from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, UserActivity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'is_active', 'password', 'first_name', 'last_name']
        read_only_fields = ['id', 'is_staff']

    def _apply_role_flags(self, user: CustomUser):
        role = user.role
        user.is_staff = role in ('STAFF', 'MANAGER', 'ADMIN')
        user.is_superuser = role == 'ADMIN'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        self._apply_role_flags(user)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        self._apply_role_flags(instance)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Verifica que la nueva contraseña y su confirmación coincidan.
        """
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "Las nuevas contraseñas no coinciden."})
                
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token serializer that injects the authenticated user's role into the access token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active']
        read_only_fields = ['id', 'username', 'role', 'is_staff', 'is_active']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'allow_blank': True, 'required': False},
            'last_name': {'allow_blank': True, 'required': False},
        }

    def validate_email(self, value):
        user = self.instance
        if user and CustomUser.objects.exclude(pk=user.pk).filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        fields_to_update = []

        if email is not None:
            instance.email = email.strip()
            fields_to_update.append('email')

        if first_name is not None:
            instance.first_name = first_name.strip()
            fields_to_update.append('first_name')

        if last_name is not None:
            instance.last_name = last_name.strip()
            fields_to_update.append('last_name')

        if fields_to_update:
            instance.save(update_fields=fields_to_update)

        return instance


class AdminResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=8)


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = [
            'id',
            'method',
            'path',
            'status_code',
            'timestamp',
            'ip_address',
            'user_agent',
            'query_params',
            'payload',
        ]
        read_only_fields = fields
