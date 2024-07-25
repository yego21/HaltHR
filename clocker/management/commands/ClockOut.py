from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clocker.models import Clocker
from django.utils import timezone
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Get the user instance
        user = User.objects.get(username='user2')

        # Check if the user already has a time_in recorded
        existing_clocker = Clocker.objects.filter(user=user, time_in__isnull=False, time_out__isnull=True).first()

        if existing_clocker:
            # User has a time_in recorded but no time_out yet
            existing_clocker.time_out = timezone.now()
            existing_clocker.save()
            self.stdout.write(self.style.SUCCESS(f'Clock out time recorded for {user.username}'))
        else:
            # User does not have a time_in recorded, record new clock in

            self.stdout.write(self.style.SUCCESS(f'{user.username} does not have Clock in record for today, are you sure to Clock out?'))
            choice = input("Choose an option (y or n): ")
            if choice == 'y':
                time_out = timezone.now()
                clocker = Clocker(user=user, time_out=time_out)
                clocker.save()
                self.stdout.write(self.style.SUCCESS(f'Clock out time recorded for {user.username}'))
            elif choice == 'n':
                print("Clock out action cancelled.")
            else:
                print("Invalid choice.")