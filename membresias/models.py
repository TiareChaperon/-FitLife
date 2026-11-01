from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Plan(models.Model):

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField(blank=True)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duracion_dias = models.PositiveIntegerField()

    activo = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        errores = {}

        if self.precio is not None and self.precio <= 0:
            errores['precio'] = 'El precio debe ser mayor que cero.'

        if self.duracion_dias is not None and self.duracion_dias <= 0:
            errores['duracion_dias'] = 'La duración debe ser mayor que cero días.'

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return self.nombre


class Membresia(models.Model):

    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('VENCIDA', 'Vencida'),
        ('CONGELADA', 'Congelada'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='membresias'
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='membresias'
    )

    fecha_inicio = models.DateField()

    fecha_termino = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVA'
    )

    def clean(self):
        super().clean()

        if self.fecha_inicio and self.fecha_termino:
            if self.fecha_termino < self.fecha_inicio:
                raise ValidationError({
                    'fecha_termino': 'La fecha de término no puede ser anterior a la fecha de inicio.'
                })

    def __str__(self):
        return f"{self.cliente.username} - {self.plan.nombre}"


class Pago(models.Model):

    METODOS = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    ESTADOS = [
        ('PAGADO', 'Pagado'),
        ('PENDIENTE', 'Pendiente'),
        ('ANULADO', 'Anulado'),
    ]

    membresia = models.ForeignKey(
        Membresia,
        on_delete=models.CASCADE,
        related_name='pagos'
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def clean(self):
        super().clean()

        if self.monto is not None and self.monto <= 0:
            raise ValidationError({
                'monto': 'El monto del pago debe ser mayor que cero.'
            })

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    metodo = models.CharField(
        max_length=20,
        choices=METODOS
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PAGADO'
    )

    def __str__(self):
        return f"Pago {self.id} - {self.membresia.cliente.username}"
