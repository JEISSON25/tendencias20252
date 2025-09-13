from django.db import models

# Create your models here.
class Recursos(models.Model):
    id_recurso = models.CharField("ID o Código de Recurso",primary_key=True,max_length=15)
    nombre_recurso = models.CharField("Nombre del recurso", max_length=50)
    TIPOS_RECURSOS = [
        ("SALA", "Sala de Reuniones"),
        ("PC","Computador Portátil"),
        ("PYT","Proyector"),
        ("TV","Televisor"),
        ("MON","Monitor para PC"),
        ("HRRM","Herramienta")
    ]
    tipo_recurso = models.CharField(max_length=4,choices=TIPOS_RECURSOS)
    ESTADOS_RECURSOS = [
        ("DISPONIBLE", "Disponible para reserva"),
        ("USO","En uso"),
        ("MANTENIMIENTO","En Mantenimiento")
    ]
    estado_recurso = models.CharField(max_length=13,choices=ESTADOS_RECURSOS, default="DISPONIBLE")
    UBICACIONES_RECURSOS = [
        ("SUR", "Bloque Sur"),
        ("NORTE","Bloque Norte"),
        ("CENTRO","Bloque Centro")
    ]
    ubicacion_recurso = models.CharField(max_length=6,choices=UBICACIONES_RECURSOS)
    descripcion_recurso = models.CharField("Descripción",max_length=150, null=True)
    def __str__(self):
        return f"{self.id_recurso} - {self.nombre_recurso} - {self.tipo_recurso} - {self.estado_recurso} - {self.ubicacion_recurso} - {self.descripcion_recurso}"
