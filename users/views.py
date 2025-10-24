from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import AdminUserSerializer, ChangePasswordSerializer, UserSerializer
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserManagementViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser] 
    serializer_class = AdminUserSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    Vista para cambiar la contraseña del usuario autenticado.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        """Devuelve el objeto CustomUser del usuario autenticado."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Contraseña actual incorrecta."]},
                                status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.validated_data.get("new_password")
            self.object.set_password(new_password)
            self.object.save()

            return Response({"detail": "Contraseña actualizada exitosamente."}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)