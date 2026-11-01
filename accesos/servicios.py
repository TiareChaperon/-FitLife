from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction

from accesos.models import Acceso
from membresias.models import Membresia


@transaction.atomic
def validar_acceso_qr(codigo, movimiento="ENTRADA"):
    codigo = codigo.strip()
    movimiento = movimiento.upper()

    if movimiento not in ("ENTRADA", "SALIDA"):
        return {"permitido": False, "mensaje": "Movimiento inválido."}

    if not codigo.startswith("FITLIFE-"):
        return {"permitido": False, "mensaje": "Código QR inválido."}

    identificador = codigo.removeprefix("FITLIFE-")

    if not identificador.isdigit():
        return {"permitido": False, "mensaje": "Código QR inválido."}

    cliente = User.objects.select_for_update().filter(
        id=int(identificador)
    ).first()

    if cliente is None:
        return {"permitido": False, "mensaje": "Cliente no encontrado."}

    ultimo = Acceso.objects.filter(
        cliente=cliente,
        resultado="PERMITIDO"
    ).order_by("-fecha_hora", "-id").first()

    dentro = ultimo is not None and ultimo.tipo_movimiento == "ENTRADA"

    if movimiento == "ENTRADA":
        hoy = timezone.localdate()

        membresia = Membresia.objects.filter(
            cliente=cliente,
            estado="ACTIVA",
            fecha_inicio__lte=hoy,
            fecha_termino__gte=hoy
        ).filter(
            pagos__estado="PAGADO"
        ).distinct().first()

        membresia_vigente = Membresia.objects.filter(
            cliente=cliente,
            estado="ACTIVA",
            fecha_inicio__lte=hoy,
            fecha_termino__gte=hoy
        ).exists()

        if dentro:
            permitido = False
            mensaje = "Acceso denegado: el cliente ya está dentro."
        elif not membresia_vigente:
            permitido = False
            mensaje = "Acceso denegado: membresía no vigente."
        elif membresia is None:
            permitido = False
            mensaje = "Acceso denegado: no registra un pago confirmado."
        else:
            permitido = True
            mensaje = "Entrada permitida."

    else:
        permitido = dentro
        mensaje = (
            "Salida registrada correctamente."
            if permitido
            else "Salida denegada: el cliente no está dentro."
        )

    Acceso.objects.create(
        cliente=cliente,
        codigo_qr=codigo,
        tipo_movimiento=movimiento,
        resultado="PERMITIDO" if permitido else "DENEGADO",
        motivo=mensaje
    )

    return {
        "permitido": permitido,
        "mensaje": mensaje,
        "cliente": cliente.username
    }
