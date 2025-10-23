from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from apps.usuarios.views import UsuariosViewSet
from apps.roles.views import RolesViewSet
from apps.reservas.views import ReservasViewSet,export_reservas_to_pdf,export_reservas_to_json
from apps.recursos.views import RecursosViewSet,export_recursos_to_pdf,export_recursos_to_json

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Gestión de Recursos API",
      default_version='v1',
      description="Documentación de la API del proyecto Gestión de Recursos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="soporte@ejemplo.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # 👈 en prod conviene restringir
)

# Rutas API
router = routers.DefaultRouter()
router.register(r'usuarios', UsuariosViewSet)
router.register(r'roles', RolesViewSet)
router.register(r'reservas', ReservasViewSet)
router.register(r'recursos', RecursosViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('export/recursos/pdf',export_recursos_to_pdf,name='export_recursos_to_pdf'),
    path('export/recursos/json',export_recursos_to_json,name='export_recursos_to_json'),
     path('export/reservas/json',export_reservas_to_json,name='export_reservas_to_json'),
     path('export/reservas/pdf',export_reservas_to_pdf,name='export_reservas_to_pdf'),
    # Rutas Swagger y ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), 
         name='token_refresh'),
     path('api-auth/', include('rest_framework.urls'))
]
