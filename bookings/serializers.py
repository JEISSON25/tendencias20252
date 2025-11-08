# bookings/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ServiceType, ServiceInstance, Booking, Discount
from datetime import datetime
from drf_spectacular.utils import extend_schema_field

User = get_user_model()

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceInstanceSerializer(serializers.ModelSerializer):
    service_type_detail = ServiceTypeSerializer(source='service_type', read_only=True)
    price_per_hour = serializers.SerializerMethodField()

    class Meta:
        model = ServiceInstance
        fields = ['id', 'service_type', 'service_type_detail', 'name', 'description', 'price_per_hour']
        read_only_fields = ['price_per_hour', 'service_type_detail']

    @extend_schema_field(serializers.CharField)
    def get_price_per_hour(self, obj):
        service_type = obj.service_type
        if service_type and service_type.cost_per_hour is not None:
            return service_type.cost_per_hour
        return None

class DiscountSerializer(serializers.ModelSerializer):
    service_type_detail = ServiceTypeSerializer(source='service_type', read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'service_type', 'service_type_detail', 'description', 'discount_percentage', 'is_active']
        read_only_fields = ['service_type_detail']

class BookingUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):
        name = obj.get_full_name()
        return name.strip() or ''


class BookingSerializer(serializers.ModelSerializer):
    service_instance = serializers.PrimaryKeyRelatedField(queryset=ServiceInstance.objects.all())
    service_instance_detail = ServiceInstanceSerializer(source='service_instance', read_only=True)
    user_detail = BookingUserSerializer(source='user', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'user_detail',
            'service_instance',
            'service_instance_detail',
            'start_time',
            'end_time',
            'duration_hours',
            'cost',
            'discount',
            'final_cost',
            'created_at',
            'status',
        ]
        read_only_fields = ['user', 'user_detail', 'duration_hours', 'cost', 'discount', 'final_cost', 'created_at', 'status']

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
            end_time__gt=start_time,
            status=Booking.STATUS_ACTIVE,
        ).exists()

        if conflicting_booking:
            raise serializers.ValidationError("Este servicio no está disponible en el horario seleccionado.")

        return data


class BookingSummarySerializer(serializers.ModelSerializer):
    space = serializers.CharField(source='service_instance.name')
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'space', 'start_time', 'end_time', 'status', 'customer']

    @extend_schema_field(serializers.CharField)
    def get_customer(self, obj):
        full_name = obj.user.get_full_name()
        return full_name.strip() if full_name else obj.user.username

class AdminDashboardMetricsSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    total_hours = serializers.FloatField()
    occupancy_rate = serializers.FloatField()
    upcoming_count = serializers.IntegerField()
    revenue = serializers.FloatField()