from apps.logs.models import Log

def crear_log(usuario, status="success", level="sistema", message=""):

    if usuario is None:
        raise ValueError("No se puede crear un log sin un usuario autenticado.")

    return Log.objects.create(
        usuario=usuario,
        status=status,
        level=level,
        message=message
    )
