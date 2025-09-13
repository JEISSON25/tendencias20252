from rest_framework import viewsets
from .models import Reservas
from .serializers import ReservasSerializer

class ReservasViewSet(viewsets.ModelViewSet):
    queryset = Reservas.objects.all()
    serializer_class = ReservasSerializer