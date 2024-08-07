from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField
# from employee.models import UserProfile


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,)
    department_head = models.ForeignKey('employee.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_departments')



    def get_members(self):
        from employee.models import UserProfile
        return UserProfile.objects.filter(department=self)

    get_members.short_description = 'Members'



    # my_list = ArrayField(models.CharField(max_length=100), blank=True, default=member_list)










    def __str__(self):
        return self.name






class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title









