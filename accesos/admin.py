from django.contrib import admin
from .models import Acceso


@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'codigo_qr',
        'tipo_movimiento',
        'fecha_hora',
        'resultado',
        'motivo'
    )
    list_filter = ('resultado', 'tipo_movimiento')
    search_fields = ('cliente__username', 'codigo_qr')
