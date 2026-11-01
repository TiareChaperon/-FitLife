from django.shortcuts import render


def inicio(request):
    return render(request, 'dashboard/inicio.html')


from accounts.permisos import personal_requerido
from django.shortcuts import render
from dashboard.servicios import obtener_aforo_actual


@personal_requerido
def dashboard_aforo(request):
    aforo = obtener_aforo_actual()

    return render(
        request,
        'dashboard/aforo.html',
        {
            'total_personas': aforo['total'],
            'personas': aforo['personas'],
        }
    )
