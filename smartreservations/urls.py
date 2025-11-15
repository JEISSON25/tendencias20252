from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from users.views import (
    AdminUserViewSet,
    ChangePasswordView,
    CurrentUserView,
    CustomTokenObtainPairView,
    UserActivityListView,
    RegisterView,
)
from bookings.api.service_type import ServiceTypeViewSet
from bookings.api.service_instance import ServiceInstanceViewSet
from bookings.api.discount import DiscountViewSet
from bookings.api.booking import BookingViewSet, BookingReportViewSet
from bookings.api.dashboard import AdminDashboardMetricsView, AdminUpcomingBookingsView


router = DefaultRouter()
router.register(r'service-types', ServiceTypeViewSet, basename='service-type')
router.register(r'service-instances', ServiceInstanceViewSet, basename='service-instance')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'booking-reports', BookingReportViewSet, basename='booking-report')
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/auth/profile/', CurrentUserView.as_view(), name='auth_profile'),
    path('api/me/activity/', UserActivityListView.as_view(), name='user_activity'),
    path('api/admin/dashboard/metrics/', AdminDashboardMetricsView.as_view(), name='admin_dashboard_metrics'),
    path('api/admin/dashboard/upcoming-bookings/', AdminUpcomingBookingsView.as_view(), name='admin_dashboard_upcoming'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),    
    path('api/', include(router.urls)), 
]
