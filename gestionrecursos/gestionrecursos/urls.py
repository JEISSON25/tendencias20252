from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from apps.usuarios.views import UsuariosViewSet
from apps.roles.views import RolesViewSet
from apps.reservas.views import ReservasViewSet
from apps.recursos.views import RecursosViewSet

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

    # Rutas Swagger y ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
