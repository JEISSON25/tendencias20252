from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Una clase base para permisos comunes
class CustomPermissionMixin:
    def get_permissions(self):
        """
        Define permisos comunes basados en la acción.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]