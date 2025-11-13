# tendencias20252

# Ejemplo de uso de los logs
# En cualquier vista o lógica de negocio
    from apps.logs.models import Log
# 1) Registrar éxito (por ejemplo, al crear un usuario)

    Log.objects.create(
        status='success', # 'success' | 'error' | 'warning'
        level='usuarios',  # 'usuarios' | 'roles' | 'recursos' | 'reservas' | 'sistema' | 'otro'
        message='Usuario creado correctamente',
        usuario=request.user # puede ser None si es un proceso del sistema
    )

# 2) Registrar error (capturando excepciones)
    try:
        crear_reserva()
        Log.objects.create(
                status='success',
                level='reservas',
                message='Reserva creada'
        )
    except Exception as e:
        Log.objects.create(
            status='error',
            level='reservas',
            message=f'Error creando reserva: {e}',
            usuario=getattr(request, 'user', None)
        )

# 3) Consultar los últimos 5 logs del sistema
    ultimos = Log.objects.filter(level='sistema').order_by('-fecha_hora')[:5]
