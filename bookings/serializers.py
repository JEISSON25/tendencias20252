# bookings/serializers.py
from rest_framework import serializers
from .models import ServiceType, ServiceInstance, Booking, Discount
from datetime import datetime

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceInstance
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'        

class BookingSerializer(serializers.ModelSerializer):
    service_instance = serializers.PrimaryKeyRelatedField(queryset=ServiceInstance.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'user', 'service_instance', 'start_time', 'end_time', 'duration_hours', 'cost', 'discount', 'final_cost', 'created_at']
        read_only_fields = ['user', 'duration_hours', 'cost', 'discount', 'final_cost', 'created_at']

    def validate(self, data):
        """
        Valida que la reserva no se superponga con otras existentes.
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        service_instance = data.get('service_instance')

        # 1. Validar que la fecha de inicio no sea en el pasado
        if start_time < datetime.now().astimezone(start_time.tzinfo):
            raise serializers.ValidationError("La fecha de inicio no puede ser en el pasado.")
        
        # 2. Validar que la fecha de fin sea posterior a la de inicio
        if end_time <= start_time:
            raise serializers.ValidationError("La hora de finalización debe ser posterior a la de inicio.")

        # 3. Validar la disponibilidad de la ServiceInstance
        conflicting_booking = Booking.objects.filter(
            service_instance=service_instance,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if conflicting_booking:
            raise serializers.ValidationError("Este servicio no está disponible en el horario seleccionado.")

        return data