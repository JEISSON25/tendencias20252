from users.models import MovimientoUsuario
from rest_framework.request import Request 

def registrar_movimiento(request: Request, actividad: str, detalle: str = None):
    """Guarda un registro de actividad para el usuario autenticado (request.user)."""
    usuario_a_guardar = request.user if request.user.is_authenticated else None
        
    try:
        MovimientoUsuario.objects.create(
            usuario=usuario_a_guardar,
            actividad=actividad,
            detalle=detalle
        )
    except Exception as e:
        print(f"ERROR AL REGISTRAR ACTIVIDAD: {e}")