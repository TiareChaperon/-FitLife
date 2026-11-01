from django.core.management.base import BaseCommand
from membresias.servicios import actualizar_membresias_vencidas


class Command(BaseCommand):
    help = "Actualiza las membresías vencidas de FitLife"

    def handle(self, *args, **options):
        cantidad = actualizar_membresias_vencidas()

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado. Membresías actualizadas: {cantidad}"
            )
        )
