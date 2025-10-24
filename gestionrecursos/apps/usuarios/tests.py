from django.test import TestCase
from ..roles.models import Roles
from .models import Usuarios

# Create your tests here.

class  UserModelTest(TestCase):
    def setUp(self):
        self.admin_rol = Roles.objects.create(
            id_rol=1,
            nombre_rol="admin",
            descripcion_rol="Administrador"
        )
       
    def test_user_creation(self):
        """Test para crear un usuario valido"""
        user = Usuarios.objects.create(
            username="testuser",
            password="testpass123",
            rol=self.admin_rol
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.rol.nombre_rol, "admin")

    def test_user_delete(self):
        """Test para eliminar un usuario"""
        user = Usuarios.objects.create(
            username="deleteuser",
            password="deletepass123",
            rol=self.admin_rol
        )
        user_id = user.id
        user.delete()
        with self.assertRaises(Usuarios.DoesNotExist):
            Usuarios.objects.get(id=user_id)    

    def test_user_update(self):
        """Test para actualizar un usuario"""
        user = Usuarios.objects.create(
            username="updateuser",
            password="updatepass123",
            rol=self.admin_rol
        )
        user.username = "updateduser"
        user.save()
        updated_user = Usuarios.objects.get(id=user.id)
        self.assertEqual(updated_user.username, "updateduser")