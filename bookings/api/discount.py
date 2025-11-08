from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bookings.models import Discount
from bookings.serializers import DiscountSerializer

from bookings.views import CustomPermissionMixin, STAFF_PERMISSIONS

class DiscountViewSet(CustomPermissionMixin, viewsets.ModelViewSet):

    permission_required_map = {
        'list': STAFF_PERMISSIONS,
        'retrieve': STAFF_PERMISSIONS,
        'create': STAFF_PERMISSIONS,
        'update': STAFF_PERMISSIONS,
        'partial_update': STAFF_PERMISSIONS,
        'destroy': STAFF_PERMISSIONS,
        'toggle_active': STAFF_PERMISSIONS,
    }

    queryset = Discount.objects.all().select_related('service_type')
    serializer_class = DiscountSerializer

    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        discount = self.get_object()
        is_active = request.data.get('is_active')

        if is_active is not None:
            discount.is_active = bool(is_active)
        else:
            discount.is_active = not discount.is_active

        discount.save()
        serializer = self.get_serializer(discount)
        return Response(serializer.data, status=status.HTTP_200_OK)
