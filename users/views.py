from datetime import datetime, time

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    AdminUserSerializer,
    AdminResetPasswordSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CurrentUserSerializer,
    UserSerializer,
    UserActivitySerializer,
)
from .models import CustomUser, UserActivity


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        user = self.get_object()
        serializer = AdminResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)

class ChangePasswordView(generics.UpdateAPIView):
    """
    Vista para cambiar la contraseña del usuario autenticado.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        """Devuelve el objeto CustomUser del usuario autenticado."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Contraseña actual incorrecta."]},
                                status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.validated_data.get("new_password")
            self.object.set_password(new_password)
            self.object.save()

            return Response({"detail": "Contraseña actualizada exitosamente."}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Provide JWT tokens enriched with the user's role in the access token payload.
    """

    serializer_class = CustomTokenObtainPairSerializer


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    Returns and updates the profile data for the authenticated user.
    """

    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserActivityListView(generics.ListAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserActivity.objects.filter(user=self.request.user)
        params = self.request.query_params

        method = params.get('method')
        if method:
            queryset = queryset.filter(method__iexact=method.upper())

        status_code = params.get('status_code')
        if status_code and status_code.isdigit():
            queryset = queryset.filter(status_code=int(status_code))

        search = params.get('search')
        if search:
            queryset = queryset.filter(Q(path__icontains=search) | Q(query_params__icontains=search))

        start = self._parse_date_param(params.get('start'))
        if start:
            queryset = queryset.filter(timestamp__gte=start)

        end = self._parse_date_param(params.get('end'), end_of_day=True)
        if end:
            queryset = queryset.filter(timestamp__lte=end)

        return queryset.order_by('-timestamp')

    def _parse_date_param(self, value: str | None, end_of_day: bool = False):
        if not value:
            return None

        dt = parse_datetime(value)
        if not dt:
            parsed_date = parse_date(value)
            if not parsed_date:
                return None
            dt = datetime.combine(
                parsed_date,
                time.max if end_of_day else time.min,
            )

        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
