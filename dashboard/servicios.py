from django.db.models import OuterRef, Subquery

from accesos.models import Acceso


def obtener_aforo_actual():
    ultimo_movimiento = (
        Acceso.objects
        .filter(
            cliente_id=OuterRef('cliente_id'),
            resultado='PERMITIDO'
        )
        .order_by('-fecha_hora', '-id')
        .values('id')[:1]
    )

    personas_dentro = (
        Acceso.objects
        .filter(
            resultado='PERMITIDO',
            tipo_movimiento='ENTRADA',
            id=Subquery(ultimo_movimiento)
        )
        .select_related('cliente')
        .order_by('cliente__username')
    )

    return {
        'total': personas_dentro.count(),
        'personas': personas_dentro,
    }
