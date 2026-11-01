from django.core.management.base import BaseCommand
from clases.servicios import actualizar_clases_finalizadas


class Command(BaseCommand):
    help = "Actualiza las clases finalizadas de FitLife"

    def handle(self, *args, **options):
        cantidad = actualizar_clases_finalizadas()

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado. Clases actualizadas: {cantidad}"
            )
        )
