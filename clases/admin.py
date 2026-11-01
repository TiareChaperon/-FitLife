from django.contrib import admin
from .models import Clase, Reserva, ListaEspera


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'instructor',
        'fecha_hora',
        'capacidad',
        'estado'
    )
    list_filter = ('estado',)
    search_fields = ('nombre', 'instructor')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'clase',
        'fecha_reserva',
        'estado'
    )
    list_filter = ('estado',)
    search_fields = ('cliente__username', 'clase__nombre')


@admin.register(ListaEspera)
class ListaEsperaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'clase',
        'posicion',
        'fecha_ingreso',
        'estado'
    )
    list_filter = ('estado',)
    search_fields = ('cliente__username', 'clase__nombre')
    ordering = ('posicion',)
