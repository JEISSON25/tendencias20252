from rest_framework import permissions

# --- Clase de Permiso Genérica (opcional, pero útil) ---
# Usamos un mixin para simplificar la verificación de autenticación
class BaseRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Todos los permisos personalizados requieren que el usuario esté autenticado
        return request.user.is_authenticated

# --- Roles Específicos ---

class IsClient(BaseRolePermission):
    """Permite el acceso solo si el usuario tiene el rol 'CLIENT'."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role == 'CLIENT'

class IsStaffOrManager(BaseRolePermission):
    """Permite el acceso a roles de Staff, Gerente o Administrador."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
            
        # Utilizamos la lógica de roles definidos
        return request.user.role in ['STAFF', 'MANAGER', 'ADMIN']

class IsManager(BaseRolePermission):
    """Permite el acceso solo a Gerentes o Administradores (usado para acciones de alto nivel)."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
            
        return request.user.role in ['MANAGER', 'ADMIN']