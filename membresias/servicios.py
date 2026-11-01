from django.utils import timezone

from membresias.models import Membresia


def actualizar_membresias_vencidas():
    """
    Marca como VENCIDA las membresías ACTIVAS
    cuya fecha de término ya pasó.

    No modifica membresías CONGELADAS.
    """
    hoy = timezone.localdate()

    cantidad = Membresia.objects.filter(
        estado='ACTIVA',
        fecha_termino__lt=hoy
    ).update(estado='VENCIDA')

    return cantidad
