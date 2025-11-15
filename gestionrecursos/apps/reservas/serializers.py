from rest_framework import serializers
from .models import Reservas

class ReservasSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    recurso = serializers.SerializerMethodField()


    def get_usuario(self, obj):
        if obj.id_user:
            return {
                'nombre': obj.id_user.username
            }
        return None
    
    def get_recurso(self, obj):
        if obj.id_recurso:
            return {
                'nombre': obj.id_recurso.nombre_recurso
            }
        return None 
    

    class Meta:
        model = Reservas
        fields = "__all__"
 