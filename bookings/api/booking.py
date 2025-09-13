from decimal import Decimal

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from ..services.reports import generate_json_report, generate_pdf_report

from bookings.views import CustomPermissionMixin
from bookings.services.email_service import EmailService

class BookingViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        # EmailService.send_booking_confirmation_email(booking)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        self.perform_destroy(booking)
        
        EmailService.send_booking_cancellation_email(booking)

        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingReportViewSet(CustomPermissionMixin, viewsets.GenericViewSet):
    @extend_schema(
        summary="Genera un reporte en formato PDF.",
        description="Este endpoint devuelve un reporte de los datos en formato PDF.",
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='pdf')
    def report_pdf(self, request):
        queryset = Booking.objects.all()
        return generate_pdf_report(queryset)        

    @extend_schema(
        summary="Genera un reporte en formato JSON.",
        description="Este endpoint devuelve un reporte de los datos en formato JSON.",
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='json')
    def report_json(self, request):
        queryset = Booking.objects.all()
        return generate_json_report(queryset)