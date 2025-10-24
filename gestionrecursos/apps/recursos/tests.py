from django.test import TestCase
from .models import Recursos

# Create your tests here.

class  RecursoModelTest(TestCase):
      
    def test_recurso_creation(self):
        """Test para crear un recurso valido"""
        recurso = Recursos.objects.create(
            id_recurso="R001",
            nombre_recurso = "Proyector Epson",
            tipo_recurso="SALA",
            estado_recurso="DISPONIBLE",
            ubicacion_recurso="SUR",
            descripcion_recurso="Sala de conferencias principal"
        )
        self.assertEqual(recurso.id_recurso, "R001")
        self.assertEqual(recurso.nombre_recurso, "Proyector Epson")

    def test_recurso_delete(self):
        """Test para eliminar un recurso"""
        recurso = Recursos.objects.create(
            id_recurso="R002",
            nombre_recurso = "Laptop Dell",
            tipo_recurso="PC",
            estado_recurso="DISPONIBLE",
            ubicacion_recurso="NORTE",
            descripcion_recurso="Computador portátil para presentaciones"
        )
        recurso_id = recurso.id_recurso
        recurso.delete()
        with self.assertRaises(Recursos.DoesNotExist):
            Recursos.objects.get(id_recurso=recurso_id)

    def test_recurso_update(self):
        """Test para actualizar un recurso"""
        recurso = Recursos.objects.create(
            id_recurso="R003",
            nombre_recurso = "Sala de Reuniones A",
            tipo_recurso="SALA",
            estado_recurso="DISPONIBLE",
            ubicacion_recurso="ESTE",
            descripcion_recurso="Sala de reuniones pequeña"
        )
        recurso.estado_recurso = "MANTENIMIENTO"
        recurso.save()
        updated_recurso = Recursos.objects.get(id_recurso="R003")
        self.assertEqual(updated_recurso.estado_recurso, "MANTENIMIENTO")