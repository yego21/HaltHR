# employee/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from company.models import Department




class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)



    def __str__(self):
        return self.name




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def is_department_head(self):
        if self.department:
                if self.department.department_head == self:
                    # return f'{self.user.username} {self.department.department_head}'
                    return 'Department Head'
                else:
                    return 'Member'
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


    hire_date = models.DateField(default='1970-01-01')
    # is_department_head = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # Department = models.ForeignKey()



    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

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
