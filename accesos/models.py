from django.db import models
from django.contrib.auth.models import User


class Acceso(models.Model):

    RESULTADOS = [
        ('PERMITIDO', 'Permitido'),
        ('DENEGADO', 'Denegado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accesos'
    )

    tipo_movimiento = models.CharField(
        max_length=10,
        choices=[
            ('ENTRADA', 'Entrada'),
            ('SALIDA', 'Salida'),
        ],
        default='ENTRADA'
    )

    codigo_qr = models.CharField(
        max_length=100
    )

    fecha_hora = models.DateTimeField(
        auto_now_add=True
    )

    resultado = models.CharField(
        max_length=20,
        choices=RESULTADOS
    )

    motivo = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.cliente.username} - {self.resultado} - {self.fecha_hora}"
