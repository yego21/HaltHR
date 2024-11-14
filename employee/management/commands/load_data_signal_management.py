from django.core.management.base import BaseCommand
from django.core.management import call_command
from employee.signals import disable_signals, enable_signals

class Command(BaseCommand):
    help = 'Load data while controlling signal management'

    def handle(self, *args, **kwargs):
        # Disable signals before loading data
        disable_signals()

        # Load the data (you can load your User, Company, and other models here)
        call_command('loaddata', 'testdump.json')  # Modify as necessary


        # Re-enable signals after loading
        enable_signals()

        self.stdout.write(self.style.SUCCESS('Successfully loaded data and managed signals.'))