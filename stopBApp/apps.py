from django.apps import AppConfig
from django.db.utils import OperationalError
from django.core.management import call_command

class StopbappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stopBApp'

    def ready(self):
        from stopBApp.utils import sync_bus_lines
        try:
            call_command('check')
            sync_bus_lines()
        except OperationalError:
            print("Database is not ready yet. Skipping bus line sync.")
