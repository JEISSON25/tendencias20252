from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from bookings.models import ServiceInstance
from bookings.serializers import ServiceInstanceSerializer

from bookings.views import CustomPermissionMixin

class ServiceInstanceViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    queryset = ServiceInstance.objects.all()
    serializer_class = ServiceInstanceSerializer