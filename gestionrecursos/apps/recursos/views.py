from rest_framework import viewsets
from .models import Recursos
from .serializers import RecursosSerializer

class RecursosViewSet(viewsets.ModelViewSet):
    queryset = Recursos.objects.all()
    serializer_class = RecursosSerializer
