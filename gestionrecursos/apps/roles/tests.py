from django.test import TestCase
from .models import Roles

class  RolesModelTest(TestCase):

    def test_rol_creation(self):
        """Test para crear un rol valido"""
        rol = Roles.objects.create(
            id_rol=1,
            nombre_rol="admin",
            descripcion_rol="Administrador"
        )
        self.assertEqual(rol.id_rol, 1)
        self.assertEqual(rol.nombre_rol, "admin")

    def test_rol_delete(self):
        """Test para eliminar un rol"""
        rol = Roles.objects.create(
            id_rol=2,
            nombre_rol="user",
            descripcion_rol="Usuario"
        )
        rol_id = rol.id_rol
        rol.delete()
        with self.assertRaises(Roles.DoesNotExist):
            Roles.objects.get(id_rol=rol_id)   

    def test_rol_update(self):
        """Test para actualizar un rol"""
        rol = Roles.objects.create(
            id_rol=3,
            nombre_rol="guest",
            descripcion_rol="Invitado"
        )
        rol.nombre_rol = "visitor"
        rol.save()
        updated_rol = Roles.objects.get(id_rol=3)
        self.assertEqual(updated_rol.nombre_rol, "visitor")        

