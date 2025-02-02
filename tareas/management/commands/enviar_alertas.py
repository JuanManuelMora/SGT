from django.core.management.base import BaseCommand
from tareas.views import enviar_alertas_tareas

class Command(BaseCommand):
    help = "Envia alertas de tareas próximas a vencer"

    def handle(self, *args, **kwargs):
        enviar_alertas_tareas()
        self.stdout.write("✅ Alertas enviadas correctamente.")