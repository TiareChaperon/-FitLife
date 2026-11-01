from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction 

class Clase(models.Model):

    ESTADOS = [
        ('PROGRAMADA', 'Programada'),
        ('CANCELADA', 'Cancelada'),
        ('FINALIZADA', 'Finalizada'),
    ]

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField(blank=True)

    instructor = models.CharField(max_length=100)

    fecha_hora = models.DateTimeField()

    capacidad = models.PositiveIntegerField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PROGRAMADA'
    )

    def __str__(self):
        return f"{self.nombre} - {self.fecha_hora}"


class Reserva(models.Model):

    ESTADOS = [
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    fecha_reserva = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='CONFIRMADA'
    )
    def clean(self):
        super().clean()

        if not self.clase_id or self.estado != 'CONFIRMADA':
            return

        reservas = Reserva.objects.filter(
            clase_id=self.clase_id,
            estado='CONFIRMADA'
        )

        if self.pk:
            reservas = reservas.exclude(pk=self.pk)

        if reservas.count() >= self.clase.capacidad:
            raise ValidationError(
                "Esta clase ya no tiene cupos disponibles."
            )

    def save(self, *args, **kwargs):
        estaba_confirmada = False

        if self.pk:
            estado_anterior = Reserva.objects.filter(
                pk=self.pk
            ).values_list('estado', flat=True).first()

            estaba_confirmada = estado_anterior == 'CONFIRMADA'

        with transaction.atomic():
            super().save(*args, **kwargs)

            if estaba_confirmada and self.estado == 'CANCELADA':
                transaction.on_commit(
                    lambda clase_id=self.clase_id: asignar_cupo_lista_espera(clase_id)
                )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'clase'],
                name='reserva_unica_cliente_clase'
            )
        ]

    def __str__(self):
        return f"{self.cliente.username} - {self.clase.nombre}"


class ListaEspera(models.Model):

    ESTADOS = [
        ('ESPERANDO', 'Esperando'),
        ('PROMOVIDO', 'Promovido'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listas_espera'
    )

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='lista_espera'
    )

    posicion = models.PositiveIntegerField()

    fecha_ingreso = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ESPERANDO'
    )

    class Meta:
        ordering = ['posicion']
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'clase'],
                condition=models.Q(estado='ESPERANDO'),
                name='espera_unica_activa_cliente_clase'
            )
        ]

    def __str__(self):
        return f"{self.cliente.username} - {self.clase.nombre} - Posición {self.posicion}"


def asignar_cupo_lista_espera(clase_id):
    with transaction.atomic():
        clase = Clase.objects.select_for_update().get(pk=clase_id)

        from django.utils import timezone

        if clase.estado != 'PROGRAMADA' or clase.fecha_hora <= timezone.now():
            return None

        confirmadas = Reserva.objects.filter(
            clase=clase,
            estado='CONFIRMADA'
        ).count()

        if confirmadas >= clase.capacidad:
            return None

        pendientes = ListaEspera.objects.filter(
            clase=clase,
            estado='ESPERANDO'
        ).order_by('posicion', 'fecha_ingreso', 'pk')

        for espera in pendientes:
            reserva, creada = Reserva.objects.get_or_create(
                cliente=espera.cliente,
                clase=clase,
                defaults={'estado': 'CANCELADA'}
            )

            if reserva.estado == 'CONFIRMADA':
                espera.estado = 'PROMOVIDO'
                espera.save(update_fields=['estado'])
                continue

            reserva.estado = 'CONFIRMADA'
            reserva.full_clean()
            reserva.save(update_fields=['estado'])

            espera.estado = 'PROMOVIDO'
            espera.save(update_fields=['estado'])

            return reserva

        return None
