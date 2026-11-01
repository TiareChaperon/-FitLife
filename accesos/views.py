from accounts.permisos import personal_requerido
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from accesos.servicios import validar_acceso_qr


@personal_requerido
@require_http_methods(["GET", "POST"])
def control_acceso(request):
    resultado = None

    if request.method == "POST":
        codigo = request.POST.get("codigo_qr", "").strip()

        if codigo:
            movimiento = request.POST.get("movimiento", "ENTRADA")
            resultado = validar_acceso_qr(codigo, movimiento)
        else:
            resultado = {
                "permitido": False,
                "mensaje": "Debes ingresar un código QR."
            }

    return render(
        request,
        "accesos/control.html",
        {"resultado": resultado}
    )
