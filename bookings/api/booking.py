from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from ..services.reports import generate_json_report, generate_pdf_report

from bookings.views import CustomPermissionMixin, AUTH_PERMISSIONS, STAFF_PERMISSIONS, CLIENT_PERMISSIONS
from bookings.services.notifications.confirmation_notifier import BookingConfirmationNotifier
from bookings.services.notifications.cancellation_notifier import BookingCancellationNotifier

class BookingViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    permission_required_map = {
        'list': AUTH_PERMISSIONS,   
        'retrieve': CLIENT_PERMISSIONS,
        'create': CLIENT_PERMISSIONS,  
        
        'update': STAFF_PERMISSIONS,
        'partial_update': STAFF_PERMISSIONS,
        'destroy': CLIENT_PERMISSIONS,

        'reports': STAFF_PERMISSIONS,
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Booking.objects.all()
        
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        notifier = BookingConfirmationNotifier()

        notifier.send_notification(booking)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        self.perform_destroy(booking)

        notifier = BookingCancellationNotifier()
        
        notifier.send_notification(booking)

        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingReportViewSet(CustomPermissionMixin, viewsets.GenericViewSet):

    permission_required_map = {
        'report_pdf': STAFF_PERMISSIONS,
        'report_json': STAFF_PERMISSIONS,
    }

    @extend_schema(
        summary="Genera un reporte en formato PDF.",
        description="Este endpoint devuelve un reporte de los datos en formato PDF.",
    )
    @action(detail=False, methods=['get'], url_path='pdf')
    def report_pdf(self, request):
        queryset = Booking.objects.all()
        return generate_pdf_report(queryset)        

    @extend_schema(
        summary="Genera un reporte en formato JSON.",
        description="Este endpoint devuelve un reporte de los datos en formato JSON.",
    )
    @action(detail=False, methods=['get'], url_path='json')
    def report_json(self, request):
        queryset = Booking.objects.all()
        return generate_json_report(queryset)