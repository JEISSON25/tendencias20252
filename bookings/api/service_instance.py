import pytz
from rest_framework import viewsets, status
from bookings.models import ServiceInstance
from bookings.serializers import ServiceInstanceSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from datetime import datetime, time, timedelta
from django.utils import timezone

from bookings.models import GlobalSettings

from bookings.views import CustomPermissionMixin, AUTH_PERMISSIONS, STAFF_PERMISSIONS

class ServiceInstanceViewSet(CustomPermissionMixin, viewsets.ModelViewSet):

    permission_required_map = {
        'list': AUTH_PERMISSIONS,
        'retrieve': AUTH_PERMISSIONS,
        'create': STAFF_PERMISSIONS,
        'update': STAFF_PERMISSIONS,
        'partial_update': STAFF_PERMISSIONS,
        'destroy': STAFF_PERMISSIONS,
        'available_slots': AUTH_PERMISSIONS,
    }
        
    queryset = ServiceInstance.objects.all()
    serializer_class = ServiceInstanceSerializer

    @extend_schema(
        summary="Obtener franjas horarias disponibles para una fecha.",
        description="Devuelve una lista de las franjas disponibles en una fecha dada.",
        parameters=[
            OpenApiParameter(name='date', type=OpenApiTypes.DATE, required=True, 
                             description='Formato YYYY-MM-DD, para la fecha a consultar.'),
        ],
        responses={200: OpenApiResponse(response={'type': 'array', 'items': {'type': 'string'}}, 
                                        description='Lista de horas de inicio disponibles (ISO 8601).')}
    )
    @action(detail=True, methods=['get'], url_path='available-slots')
    def available_slots(self, request, pk=None):
        instance = self.get_object()
        date_str = request.query_params.get('date')

        if not date_str:
            return Response({"detail": "El parámetro 'date' (YYYY-MM-DD) es requerido."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Formato de fecha inválido. Use YYYY-MM-DD."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        slots = self._get_available_slots(instance, target_date)
        
        # Devolver solo las horas de inicio en formato ISO para el frontend
        return Response([s['start_time'].isoformat() for s in slots])

    def _get_available_slots(self, instance, target_date):
        """Calcula las franjas horarias disponibles para una instancia en una fecha,
        usando la zona horaria global del sistema."""
        
        settings = GlobalSettings.load()
        
        service_tz = pytz.timezone(settings.system_time_zone) 
        
        try:
            if isinstance(settings.operating_start_time, str):
                start_time_obj = datetime.strptime(settings.operating_start_time, '%H:%M:%S').time()
            else:
                start_time_obj = settings.operating_start_time
                
            if isinstance(settings.operating_end_time, str):
                end_time_obj = datetime.strptime(settings.operating_end_time, '%H:%M:%S').time()
            else:
                end_time_obj = settings.operating_end_time
                
        except Exception:
             start_time_obj = time(9, 0)
             end_time_obj = time(18, 0)
        
        slot_duration = timedelta(minutes=settings.slot_duration_minutes) 
        
        # 2. Definir el rango operativo, AWARE de la zona horaria del SISTEMA
        start_datetime_local = service_tz.localize(datetime.combine(target_date, start_time_obj))
        end_datetime_local = service_tz.localize(datetime.combine(target_date, end_time_obj))
        
        # Convertir a UTC para la consulta a la base de datos (DB)
        start_datetime_utc = start_datetime_local.astimezone(pytz.utc)
        end_datetime_utc = end_datetime_local.astimezone(pytz.utc)

        # 3. Ajuste para Hoy (Usando la Hora Local del SISTEMA)
        now_local = timezone.now().astimezone(service_tz) 
        
        if target_date == now_local.date() and start_datetime_local < now_local:
             # ... (Lógica de redondeo del slot, sigue igual)
             time_passed = now_local - start_datetime_local
             remainder = time_passed % slot_duration
             
             if remainder != timedelta(0):
                 start_datetime_local = now_local + (slot_duration - remainder)
             else:
                 start_datetime_local = now_local
        
        # 4. Obtener las reservas existentes (usando límites UTC)
        booked_intervals = list(instance.booking_set.filter(
            start_time__lt=end_datetime_utc,
            end_time__gt=start_datetime_utc
        ).order_by('start_time').values('start_time', 'end_time')) 

        # 5. Calcular las franjas disponibles, trabajando en la zona horaria LOCAL del SISTEMA
        available_slots = []
        current_time = start_datetime_local 
        
        while current_time < end_datetime_local:
            slot_end = current_time + slot_duration 
            
            if slot_end > end_datetime_local:
                break
            
            is_booked = False
            for booking in booked_intervals:
                
                # Convertir los límites de la reserva (que están en UTC)
                # a la zona horaria local del SISTEMA.
                booked_start_local = booking['start_time'].astimezone(service_tz)
                booked_end_local = booking['end_time'].astimezone(service_tz)
                
                # ... (Lógica de superposición y avance, sigue igual)
                if booked_end_local > current_time and booked_start_local < slot_end:
                    is_booked = True
                    current_time = booked_end_local 
                    break 
            
            if not is_booked:
                available_slots.append({'start_time': current_time, 'end_time': slot_end})
                current_time = slot_end 
            
        return available_slots