from rest_framework import viewsets
from .models import Roles
from .serializers import RolesSerializer

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
