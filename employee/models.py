# employee/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from company.models import Department
from cloudinary.models import CloudinaryField

import os

# For local file storage use this
# def user_directory_path(instance, filename):
#     full_name = instance.full_name.replace(" ", "_")
#     filename = f'{instance.id}.png'
#     return os.path.join('photos', full_name, filename)

# For cloudinary file storage use this
def user_directory_path(instance):
    full_name = instance.full_name.replace(" ", "_")
    cloud_filename = f'photos/{full_name}/{instance.id}.png'
    return cloud_filename

import sys




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
    photo = CloudinaryField('image', folder=user_directory_path, default='https://res.cloudinary.com/dgee7iare/image/upload/v1731983114/photos/User_Four/123.png/tuochfczg3forerqgke5.jpg')
    # photo = models.ImageField(upload_to=user_directory_path, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(default="Member", max_length=50)
    EMPLOYMENT_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('TP', 'Temporary'),
        ('IN', 'Intern'),
        ('FR', 'Freelance'),
        ('CO', 'Consultant'),
        ('OC', 'On-call'),
        ('AP', 'Apprentice'),
        ('CA', 'Casual'),
    ]
    employment_type = models.CharField(
        max_length=2,
        choices=EMPLOYMENT_TYPES,
        default='FT',
    )
    hire_date = models.DateField(default='1970-01-01')


    @property
    def is_department_head(self, null=True):
        if self.department:
            if self.department and self.department.department_head == self:
                return True
            return False





    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
        # return self.user.username


    # def save(self, *args, **kwargs):
    #     # Update is_staff field based on is_department_head property
    #     if self.is_department_head == 'Department Head':
    #         self.user.is_staff = True
    #     else:
    #         self.user.is_staff = False
    #
    #     # Save the user instance
    #     self.user.save()
    #
    #     # Save the UserProfile instance
    #     super().save(*args, **kwargs)



    # is_department_head = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # Department = models.ForeignKey()


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


