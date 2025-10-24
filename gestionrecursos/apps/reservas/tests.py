from django.test import TestCase
from django.forms import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Reservas
from apps.usuarios.models import Usuarios
from apps.recursos.models import Recursos
from apps.roles.models import Roles

class ReservasModelTest(TestCase):
    def setUp(self):
        # Crear rol
        self.rol_admin = Roles.objects.create(
            id_rol=1,
            nombre_rol="admin",
            descripcion_rol="Administrador"
        )
        self.rol_usuario = Roles.objects.create(
            id_rol=2,
            nombre_rol="user",
            descripcion_rol="Usuario"
        )

        # Crear usuarios de prueba
        self.admin_user = Usuarios.objects.create(
            username="admin",
            password="admin123",
            rol=self.rol_admin
        )
        
        self.normal_user = Usuarios.objects.create(
            username="usuario",
            password="user123",
            rol=self.rol_usuario
        )

        # Crear recursos de prueba
        self.sala_conferencias = Recursos.objects.create(
            id_recurso="1",
            tipo_recurso="SALA",
            descripcion_recurso="Sala principal"
        )
        
        self.sala_reuniones = Recursos.objects.create(
            id_recurso="2",
            tipo_recurso="PC",
            descripcion_recurso="Computador Portátil"
        )

        # Fechas de prueba
        self.fecha_inicio = timezone.now()
        self.fecha_fin = self.fecha_inicio + timedelta(hours=2)

    def test_crear_reserva_valida(self):
        """Test para crear una reserva válida"""
        reserva = Reservas.objects.create(
            estado_reserva="PENDIENTE",
            id_user=self.normal_user,
            id_recurso=self.sala_reuniones,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin
        )
        self.assertEqual(reserva.estado_reserva, "PENDIENTE")
        self.assertEqual(reserva.id_user, self.normal_user)

    def test_delete_reserva(self):
        """Test para eliminar una reserva"""
        reserva = Reservas.objects.create(
            estado_reserva="PENDIENTE",
            id_user=self.normal_user,
            id_recurso=self.sala_reuniones,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin
        )
        reserva_id = reserva.id_reserva
        reserva.delete()
        with self.assertRaises(Reservas.DoesNotExist):
            Reservas.objects.get(id_reserva=reserva_id)

    def test_update_reserva(self):
        """Test para actualizar una reserva"""
        reserva = Reservas.objects.create(
            estado_reserva="PENDIENTE",
            id_user=self.normal_user,
            id_recurso=self.sala_reuniones,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin
        )
        reserva.estado_reserva = "CANCELADA"
        reserva.save()
        updated_reserva = Reservas.objects.get(id_reserva=reserva.id_reserva)
        self.assertEqual(updated_reserva.estado_reserva, "CANCELADA")        


    def test_validacion_fechas(self):
        """Test para validar que la fecha de inicio sea anterior a la fecha de fin"""
        with self.assertRaises(ValidationError):
            reserva = Reservas(
                estado_reserva="PENDIENTE",
                id_user=self.normal_user,
                id_recurso=self.sala_reuniones,
                fecha_inicio=self.fecha_fin,
                fecha_fin=self.fecha_inicio
            )
            reserva.clean()

    def test_validacion_sala_conferencias(self):
        """Test para validar que solo administradores pueden reservar la sala de conferencias"""
        with self.assertRaises(ValidationError):
            reserva = Reservas(
                estado_reserva="PENDIENTE",
                id_user=self.normal_user,
                id_recurso=self.sala_conferencias,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin
            )
            reserva.clean()
