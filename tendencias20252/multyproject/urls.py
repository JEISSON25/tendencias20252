# config/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # 1. Ruta administrativa
    path('admin/', admin.site.urls),
    
    # --- Estructura API (bajo /api/) ---
    # 2. Rutas de Autenticación (Login JWT y Refresh Token)
    # Endpoint: /api/auth/jwt/create/ --Login
    # Endpoint: /api/auth/jwt/blacklist --Logout
    path('api/auth/', include('djoser.urls.jwt')), 
    
    # 3. Rutas de Gestión de Usuarios (Registro, Perfil, Contraseña)
    # Endpoint: /api/register/users/
    path('api/register/', include('djoser.urls')), 
    
    # 4. Rutas de Lógica de Negocio (Tus apps)
    path('api/logistica/', include('apilogistica.urls')), 
    path('api/procesamiento/', include('procesamiento.urls')),
    
    # 5. Rutas user
    path('api/users/', include('users.urls')),
    
    # 6. Rutas de Documentación
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]