from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Clocker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return f"{self.user.first_name+' '+self.user.last_name} - {self.time_in} to {self.time_out}"


# models.py




# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username





