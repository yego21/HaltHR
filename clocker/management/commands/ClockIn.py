from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clocker.models import Clocker
from django.utils import timezone

class Command(BaseCommand):
    help = 'Records clock in or clock out time for a user'

    def handle(self, *args, **kwargs):
        # Get the user instance
        user = User.objects.get(username='user2')

        # Check if the user already has a time_in recorded
        existing_clocker = Clocker.objects.filter(user=user, time_in__isnull=False, time_out__isnull=True).first()

        if existing_clocker:
            self.stdout.write(self.style.SUCCESS(f'{user.username} have already clocked in for today, please proceed to clock out or contact your system administrator'))
        else:
            # User does not have a time_in recorded, record new clock in
            time_in = timezone.now()
            clocker = Clocker(user=user, time_in=time_in)
            clocker.save()
            self.stdout.write(self.style.SUCCESS(f'Clock in time recorded for {user.username}'))


