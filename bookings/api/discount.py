from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from bookings.models import Discount
from bookings.serializers import DiscountSerializer

from bookings.views import CustomPermissionMixin


class DiscountViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer