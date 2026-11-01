from django.utils import timezone
from clases.models import Clase


def actualizar_clases_finalizadas():
    """
    Marca como FINALIZADA las clases PROGRAMADAS
    cuya fecha y hora ya pasaron.
    """
    return Clase.objects.filter(
        estado='PROGRAMADA',
        fecha_hora__lt=timezone.now()
    ).update(estado='FINALIZADA')
