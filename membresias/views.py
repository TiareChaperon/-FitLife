from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.permisos import personal_requerido
from .models import Plan
from .forms import PlanForm
from django.views.decorators.http import require_POST
from django.db.models.deletion import ProtectedError

@personal_requerido
def lista_planes(request):
    planes = Plan.objects.all().order_by('nombre')

    return render(request, 'membresias/lista_planes.html', {
        'planes': planes
    })


@personal_requerido
def crear_plan(request):
    if request.method == 'POST':
        formulario = PlanForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'El plan se creó correctamente.'
            )

            return redirect('lista_planes')
    else:
        formulario = PlanForm()

    return render(request, 'membresias/formulario_plan.html', {
        'formulario': formulario,
        'titulo': 'Crear nuevo plan'
    })


@personal_requerido
def editar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    if request.method == 'POST':
        formulario = PlanForm(request.POST, instance=plan)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'El plan se actualizó correctamente.'
            )

            return redirect('lista_planes')

    else:
        formulario = PlanForm(instance=plan)

    return render(request, 'membresias/formulario_plan.html', {
        'formulario': formulario,
        'titulo': f'Editar plan: {plan.nombre}'
    })
@personal_requerido
@require_POST
def eliminar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    if plan.membresias.exists():
        messages.error(
            request,
            'No puedes eliminar este plan porque tiene membresías asociadas.'
        )
        return redirect('lista_planes')

    try:
        plan.delete()

        messages.success(
            request,
            'El plan se eliminó correctamente.'
        )

    except ProtectedError:
        messages.error(
            request,
            'No se puede eliminar el plan porque está siendo utilizado.'
        )

    return redirect('lista_planes')
