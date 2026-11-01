from membresias.models import Pago
from django.db.models import Count, Q
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from membresias.models import Membresia
from clases.models import Clase, Reserva
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from clases.models import ListaEspera

from django.urls import reverse_lazy

from accounts.permisos import cliente_requerido

class InicioSesionView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse_lazy('admin:index')

        return reverse_lazy('panel_cliente')

from django.contrib.auth.decorators import login_required


@cliente_requerido
def panel_cliente(request):
    membresia = (
        Membresia.objects
        .filter(cliente=request.user)
        .select_related('plan')
        .order_by('-fecha_inicio', '-id')
        .first()
    )
    reservas = (
        Reserva.objects
        .filter(cliente=request.user)
        .select_related('clase')
        .order_by('clase__fecha_hora')
    )
    clases_disponibles = (
        Clase.objects
        .filter(estado='PROGRAMADA', fecha_hora__gt=timezone.now())
        .annotate(
            ocupados=Count(
                'reservas',
                filter=Q(reservas__estado='CONFIRMADA')
            )
        )
        .order_by('fecha_hora')
    )

    clases_reservadas = set(
        reservas.filter(estado='CONFIRMADA')
        .values_list('clase_id', flat=True)
    )

    clases_en_espera = set(
        ListaEspera.objects.filter(
            cliente=request.user,
            estado='ESPERANDO'
        ).values_list('clase_id', flat=True)
    )

    for clase in clases_disponibles:
        clase.ya_reservada = clase.id in clases_reservadas
        clase.en_lista_espera = clase.id in clases_en_espera

    pagos = (
        Pago.objects
        .filter(membresia__cliente=request.user)
        .select_related('membresia__plan')
        .order_by('-fecha')
    )

    return render(request, 'accounts/panel.html', {
        'membresia': membresia,
        'reservas': reservas,
        'clases_disponibles': clases_disponibles,
        'pagos': pagos,
    })

@cliente_requerido
@require_POST
def reservar_clase(request, clase_id):
    with transaction.atomic():
        clase = get_object_or_404(
            Clase.objects.select_for_update(),
            pk=clase_id
        )

        if clase.estado != 'PROGRAMADA' or clase.fecha_hora <= timezone.now():
            messages.error(request, 'Esta clase no está disponible.')
            return redirect('panel_cliente')

        reserva = Reserva.objects.filter(
            cliente=request.user,
            clase=clase
        ).first()

        if reserva and reserva.estado == 'CONFIRMADA':
            messages.info(request, 'Ya tienes una reserva confirmada.')
            return redirect('panel_cliente')

        ocupados = Reserva.objects.filter(
            clase=clase,
            estado='CONFIRMADA'
        ).count()

        if ocupados >= clase.capacidad:
            messages.warning(request, 'La clase está llena. Puedes inscribirte en la lista de espera.')
            return redirect('panel_cliente')

        if ListaEspera.objects.filter(
            clase=clase,
            estado='ESPERANDO'
        ).exists():
            messages.warning(
                request,
                'Este cupo tiene prioridad para las personas en lista de espera.'
            )
            return redirect('panel_cliente')

        if reserva:
            reserva.estado = 'CONFIRMADA'
            reserva.full_clean()
            reserva.save(update_fields=['estado'])
        else:
            reserva = Reserva(
                cliente=request.user,
                clase=clase,
                estado='CONFIRMADA'
            )
            reserva.full_clean()
            reserva.save()

        messages.success(request, '¡Tu reserva fue confirmada!')

    return redirect('panel_cliente')

@cliente_requerido
@require_POST
def cancelar_reserva(request, reserva_id):
    with transaction.atomic():
        reserva_actual = get_object_or_404(
            Reserva,
            pk=reserva_id,
            cliente=request.user
        )

        clase = Clase.objects.select_for_update().get(
            pk=reserva_actual.clase_id
        )

        reserva = Reserva.objects.select_for_update().get(
            pk=reserva_actual.pk
        )

        if clase.estado != 'PROGRAMADA' or clase.fecha_hora <= timezone.now():
            messages.error(
                request,
                'No puedes cancelar una reserva de una clase que ya comenzó o finalizó.'
            )
            return redirect('panel_cliente')

        if reserva.estado != 'CONFIRMADA':
            messages.info(request, 'Esta reserva ya está cancelada.')
            return redirect('panel_cliente')

        reserva.estado = 'CANCELADA'
        reserva.save(update_fields=['estado'])

    messages.success(
        request,
        'Tu reserva fue cancelada correctamente.'
    )

    return redirect('panel_cliente')


@cliente_requerido
@require_POST
def ingresar_lista_espera(request, clase_id):
    with transaction.atomic():
        clase = get_object_or_404(
            Clase.objects.select_for_update(),
            pk=clase_id
        )

        if clase.estado != 'PROGRAMADA' or clase.fecha_hora <= timezone.now():
            messages.error(request, 'Esta clase no está disponible.')
            return redirect('panel_cliente')

        if Reserva.objects.filter(
            cliente=request.user,
            clase=clase,
            estado='CONFIRMADA'
        ).exists():
            messages.info(request, 'Ya tienes una reserva confirmada.')
            return redirect('panel_cliente')

        if ListaEspera.objects.filter(
            cliente=request.user,
            clase=clase,
            estado='ESPERANDO'
        ).exists():
            messages.info(request, 'Ya estás en la lista de espera.')
            return redirect('panel_cliente')

        ocupados = Reserva.objects.filter(
            clase=clase,
            estado='CONFIRMADA'
        ).count()

        if ocupados < clase.capacidad:
            messages.info(request, 'Hay cupos disponibles. Puedes reservar directamente.')
            return redirect('panel_cliente')

        ultima_posicion = (
            ListaEspera.objects.filter(
                clase=clase,
                estado='ESPERANDO',
            )
            .order_by('-posicion')
            .values_list('posicion', flat=True)
            .first()
        ) or 0

        ListaEspera.objects.create(
            cliente=request.user,
            clase=clase,
            posicion=ultima_posicion + 1,
            estado='ESPERANDO'
        )

        messages.success(request, 'Ingresaste a la lista de espera.')

    return redirect('panel_cliente')
