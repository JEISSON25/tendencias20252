from decimal import Decimal
from datetime import datetime, time, timedelta

import pytz

from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking, ServiceInstance, GlobalSettings
from bookings.permissions import IsStaffOrManager
from bookings.serializers import BookingSummarySerializer, AdminDashboardMetricsSerializer


class AdminDashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrManager]
    serializer_class = AdminDashboardMetricsSerializer

    def get(self, request):
        now = timezone.now()
        active_bookings = Booking.objects.filter(status=Booking.STATUS_ACTIVE)
        total_bookings = active_bookings.count()
        total_hours = active_bookings.aggregate(total=Sum('duration_hours'))['total'] or Decimal('0')
        upcoming_count = active_bookings.filter(start_time__gte=now).count()
        revenue = active_bookings.aggregate(total=Sum('final_cost'))['total'] or Decimal('0')
        occupancy_rate = self._calculate_occupancy_rate(active_bookings, now)

        data = {
            'total_bookings': total_bookings,
            'total_hours': float(total_hours),
            'occupancy_rate': occupancy_rate,
            'upcoming_count': upcoming_count,
            'revenue': float(revenue),
        }
        return Response(data)

    def _calculate_occupancy_rate(self, active_bookings, reference_datetime):
        service_count = ServiceInstance.objects.count()
        if service_count == 0:
            return 0.0

        settings = GlobalSettings.load()
        system_tz = pytz.timezone(settings.system_time_zone)
        ref_local = reference_datetime.astimezone(system_tz)
        day_start_local, day_end_local = self._get_operating_window(settings, ref_local.date(), system_tz)

        if day_start_local >= day_end_local:
            return 0.0

        day_start_utc = day_start_local.astimezone(pytz.utc)
        day_end_utc = day_end_local.astimezone(pytz.utc)

        overlapping_bookings = active_bookings.filter(
            Q(start_time__lt=day_end_utc) & Q(end_time__gt=day_start_utc)
        )

        booked_seconds = 0.0
        for booking in overlapping_bookings:
            booking_start_local = booking.start_time.astimezone(system_tz)
            booking_end_local = booking.end_time.astimezone(system_tz)

            overlap_start = max(booking_start_local, day_start_local)
            overlap_end = min(booking_end_local, day_end_local)

            if overlap_end > overlap_start:
                booked_seconds += (overlap_end - overlap_start).total_seconds()

        operating_seconds_per_space = (day_end_local - day_start_local).total_seconds()
        total_available_seconds = operating_seconds_per_space * service_count
        if total_available_seconds <= 0:
            return 0.0

        occupancy = (booked_seconds / total_available_seconds) * 100
        return round(min(max(occupancy, 0.0), 100.0), 2)

    def _get_operating_window(self, settings, current_date, tz):
        start_time_obj = self._parse_time_value(settings.operating_start_time) or time(9, 0)
        end_time_obj = self._parse_time_value(settings.operating_end_time) or time(18, 0)

        start_local = tz.localize(datetime.combine(current_date, start_time_obj))
        end_local = tz.localize(datetime.combine(current_date, end_time_obj))

        now_local = timezone.now().astimezone(tz)
        if current_date == now_local.date() and start_local < now_local:
            start_local = now_local

        return start_local, end_local

    @staticmethod
    def _parse_time_value(value):
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%H:%M:%S').time()
            except ValueError:
                try:
                    return datetime.strptime(value, '%H:%M').time()
                except ValueError:
                    return None
        return None


class AdminUpcomingBookingsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrManager]
    serializer_class = BookingSummarySerializer

    def get(self, request):
        now = timezone.now()
        upcoming = Booking.objects.filter(start_time__gte=now).order_by('start_time')[:10]
        serializer = self.serializer_class(upcoming, many=True)
        return Response(serializer.data)
