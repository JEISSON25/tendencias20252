from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from bookings.permissions import IsClient, IsStaffOrManager, IsManager 

AUTH_PERMISSIONS = [IsAuthenticated]
NO_PERMISSIONS = [] 

CLIENT_PERMISSIONS = [IsClient]
STAFF_PERMISSIONS = [IsStaffOrManager]
MANAGER_PERMISSIONS = [IsManager]

class CustomPermissionMixin:
    
    # Define un mapa por defecto si la subclase no lo implementa
    permission_required_map = {} 

    def get_permissions(self):
        """
        Devuelve el conjunto de clases de permisos requeridos para la acción actual.
        """
        # 1. Intenta obtener el permiso del mapa específico (que ahora usa tus nuevas constantes)
        permission_classes = self.permission_required_map.get(
            self.action,
            self.permission_classes 
        )
        
        # 2. Asegúrate de que permission_classes sea una lista iterable de clases
        if not isinstance(permission_classes, list):
            permission_classes = [permission_classes]

        # 3. Devuelve una lista de instancias de permisos
        return [permission() for permission in permission_classes]