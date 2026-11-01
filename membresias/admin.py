from django.contrib import admin
from .models import Plan, Membresia, Pago


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_dias', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'plan',
        'fecha_inicio',
        'fecha_termino',
        'estado'
    )
    list_filter = ('estado', 'plan')
    search_fields = ('cliente__username',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'membresia',
        'monto',
        'fecha',
        'metodo',
        'estado'
    )
    list_filter = ('metodo', 'estado')
    search_fields = ('membresia__cliente__username',)
