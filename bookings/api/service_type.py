from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from bookings.models import ServiceType
from bookings.serializers import ServiceTypeSerializer

from bookings.views import CustomPermissionMixin

class ServiceTypeViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAdminUser]