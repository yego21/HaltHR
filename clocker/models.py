from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Clocker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return f"{self.user.first_name+' '+self.user.last_name} - {self.time_in} to {self.time_out}"


# models.py

class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username





