from rest_framework import viewsets
from bookings.models import ServiceType
from bookings.serializers import ServiceTypeSerializer

from bookings.views import CustomPermissionMixin

from bookings.views import CustomPermissionMixin, STAFF_PERMISSIONS

class ServiceTypeViewSet(CustomPermissionMixin, viewsets.ModelViewSet):

    permission_required_map = {
        'list': STAFF_PERMISSIONS,
        'retrieve': STAFF_PERMISSIONS,
        'create': STAFF_PERMISSIONS,
        'update': STAFF_PERMISSIONS,
        'partial_update': STAFF_PERMISSIONS,
        'destroy': STAFF_PERMISSIONS,
    }
            
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
