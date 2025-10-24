from rest_framework.permissions import BasePermission, SAFE_METHODS

def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

class IsAdminOrVendedorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return in_group(request.user,'admin') or in_group(request.user,'vendedor') or request.user.is_superuser

class IsClienteOwnerOrReadOnly(BasePermission):
 
 
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if in_group(request.user,'admin') or in_group(request.user,'vendedor') or request.user.is_superuser:
            return True
        # cliente dueño: match por email
        return hasattr(obj, 'cliente') and request.user.email == getattr(obj.cliente, 'email', None)
