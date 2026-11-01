from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('CLIENTE', 'Cliente'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='CLIENTE'
    )

    codigo_qr = models.CharField(
        max_length=100,
        unique=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
