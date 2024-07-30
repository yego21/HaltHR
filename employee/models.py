# employee/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone




class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)



    def __str__(self):
        return self.name




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.user.username

# class UserShift(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_shift = models.CharField(max_length=100)
#     start_time = models.DateTimeField(default=timezone.now, null=True)
#     end_time = models.DateTimeField(default=timezone.now, null=True)
#     date = models.DateField(default=timezone.now)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.user_shift.name} - {self.date}'
from django.db import models

# Create your models here.
