from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'telefono', 'codigo_qr', 'fecha_creacion')
    list_filter = ('rol',)
    search_fields = ('usuario__username', 'codigo_qr', 'telefono')
