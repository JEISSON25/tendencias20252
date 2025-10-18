from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from users.views import RegisterView, ChangePasswordView
from bookings.api.service_type import ServiceTypeViewSet
from bookings.api.service_instance import ServiceInstanceViewSet
from bookings.api.discount import DiscountViewSet
from bookings.api.booking import BookingViewSet, BookingReportViewSet


router = DefaultRouter()
router.register(r'service-types', ServiceTypeViewSet, basename='service-type')
router.register(r'service-instances', ServiceInstanceViewSet, basename='service-instance')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'booking-reports', BookingReportViewSet, basename='booking-report')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),    
    path('api/', include(router.urls)), 
]
