from datetime import datetime, time

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
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
        'create': AUTH_PERMISSIONS,  
        
        'update': STAFF_PERMISSIONS,
        'partial_update': STAFF_PERMISSIONS,
        'destroy': STAFF_PERMISSIONS,

        'cancel': AUTH_PERMISSIONS,
        'reports': STAFF_PERMISSIONS,
    }

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.all()

        now = timezone.now()
        queryset.filter(status=Booking.STATUS_ACTIVE, end_time__lte=now).update(status=Booking.STATUS_COMPLETED)

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        status_param = self.request.query_params.get('status')
        if status_param:
            normalized_status = status_param.strip().upper()
            if normalized_status == 'ACTIVE':
                queryset = queryset.filter(status=Booking.STATUS_ACTIVE)
            elif normalized_status == 'PAST':
                queryset = queryset.exclude(status=Booking.STATUS_ACTIVE)
            elif normalized_status in dict(Booking.STATUS_CHOICES):
                queryset = queryset.filter(status=normalized_status)

        return queryset.order_by('-start_time')

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        notifier = BookingConfirmationNotifier()

        notifier.send_notification(booking)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status == Booking.STATUS_CANCELED:
            return Response({'detail': 'La reserva ya fue cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status == Booking.STATUS_COMPLETED:
            return Response({'detail': 'No es posible cancelar una reserva completada.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.STATUS_CANCELED
        booking.save(update_fields=['status'])

        notifier = BookingCancellationNotifier()
        notifier.send_notification(booking)

        return Response(BookingSerializer(booking, context={'request': request}).data, status=status.HTTP_200_OK)

class BookingReportViewSet(CustomPermissionMixin, viewsets.GenericViewSet):

    permission_required_map = {
        'report_pdf': STAFF_PERMISSIONS,
        'report_json': STAFF_PERMISSIONS,
    }

    @extend_schema(
        summary="Genera un reporte en formato PDF.",
        description="Este endpoint devuelve un reporte de los datos en formato PDF.",
    )
    @action(detail=False, methods=['get'], url_path='pdf', url_name='pdf')
    def report_pdf(self, request):
        queryset = Booking.objects.select_related('user', 'service_instance').all()
        queryset, filters_applied = self._apply_report_filters(request, queryset)
        return generate_pdf_report(queryset, filters=filters_applied)

    @extend_schema(
        summary="Genera un reporte en formato JSON.",
        description="Este endpoint devuelve un reporte de los datos en formato JSON.",
    )
    @action(detail=False, methods=['get'], url_path='json', url_name='json')
    def report_json(self, request):
        queryset = Booking.objects.all()
        return generate_json_report(queryset)

    def _apply_report_filters(self, request, queryset):
        params = request.query_params
        filters_applied = []

        status_param = params.get('status')
        if status_param:
            normalized_status = status_param.strip().upper()
            valid_statuses = dict(Booking.STATUS_CHOICES)
            if normalized_status in valid_statuses:
                queryset = queryset.filter(status=normalized_status)
                filters_applied.append(('Estado', valid_statuses[normalized_status]))

        start = self._parse_param_to_datetime(params.get('start_date'), False)
        if start:
            queryset = queryset.filter(start_time__gte=start)
            filters_applied.append(('Desde', start.strftime('%d/%m/%Y %H:%M')))

        end = self._parse_param_to_datetime(params.get('end_date'), True)
        if end:
            queryset = queryset.filter(end_time__lte=end)
            filters_applied.append(('Hasta', end.strftime('%d/%m/%Y %H:%M')))

        return queryset, filters_applied

    @staticmethod
    def _parse_param_to_datetime(value, end_of_day=False):
        if not value:
            return None

        dt = parse_datetime(value)
        if not dt:
            parsed_date = parse_date(value)
            if not parsed_date:
                return None
            dt = datetime.combine(parsed_date, time.max if end_of_day else time.min)

        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
