from django.db import models
from django.contrib.auth.models import User
from employee.models import UserProfile, Shift
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import localtime

# Create your models here.
class Clocker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    # early_or_late = models.CharField(max_length=100, null=True)


    def time_to_seconds(self, t):
        if self.time_in:
            return t.hour * 3600 + t.minute * 60 + t.second
        else:
            return None

    def seconds_to_hours_minutes(self, seconds):
        """Convert total seconds to hours and minutes."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f'{hours} hours ,{minutes} minutes'



    def calculate_time_difference(self):
        if self.time_in:
        # """Calculate the difference between two datetime.time objects in hours and minutes."""
            this_user = UserProfile.objects.get(user=self.user)
            start_time = this_user.user_shift.start_time

            # start_time_str = start_time.strftime('%H%M%S')
            # start_time_int = int(start_time_str)
            #
            #
            # time_in_str = self.time_in.strftime('%H%M%S')
            naive_time_in = timezone.make_naive(self.time_in)
            time_in_time = timezone.make_aware(naive_time_in)
            # time_in_int = int(time_in_str)

            start_time_seconds = self.time_to_seconds(start_time)
            time_in_seconds = self.time_to_seconds(time_in_time)
            print(f'start seconds {start_time_seconds}')

            difference_seconds = abs(start_time_seconds - time_in_seconds)
            if start_time_seconds > time_in_seconds:
                return f'{self.seconds_to_hours_minutes(difference_seconds)} EARLY {start_time} {time_in_time}'
            elif start_time_seconds < time_in_seconds:
                if difference_seconds < 60:
                    return 'Just on time'
                else:
                    return f'{self.seconds_to_hours_minutes(difference_seconds)} LATE'
            else:
                return 'Just on time'

            # if start_time_seconds > time_in_seconds:
            #
            #     difference_seconds = (start_time_seconds) - (time_in_seconds)
            #     return f'{self.seconds_to_hours_minutes(difference_seconds)} EARLY {start_time} {time_in_time}'
            #
            #
            # elif start_time_seconds < time_in_seconds:
            #     difference_seconds = (time_in_seconds) - (start_time_seconds)
            #     if difference_seconds < 60:
            #         return 'Just on time'
            #     else:
            #         return f'{self.seconds_to_hours_minutes(difference_seconds)} LATE'
            # else:
            #     return 'Just on time'
        else:
            return 'No time in recorded'

    def evaluate_time(self, start_time_seconds, time_in_seconds, start_time, time_in_time):
        # Calculate difference
        difference_seconds = abs(start_time_seconds - time_in_seconds)

        if start_time_seconds > time_in_seconds:
            return f'{self.seconds_to_hours_minutes(difference_seconds)} EARLY {start_time} {time_in_time}'
        elif start_time_seconds < time_in_seconds:
            if difference_seconds < 60:
                return 'Just on time'
            else:
                return f'{self.seconds_to_hours_minutes(difference_seconds)} LATE'
        else:
            return 'Just on time'

    def __str__(self):
        # Convert time_in and time_out to local time (+08:00)
        # time_in_local = localtime(self.time_in).strftime('%I:%M %p') if self.time_in else 'N/A'
        # time_out_local = localtime(self.time_out).strftime('%I:%M %p') if self.time_out else 'N/A'
        this_user = UserProfile.objects.get(user=self.user)
        return f"Name: {self.user.first_name} {self.user.last_name}___________________________Shift: {this_user.user_shift.start_time}"







