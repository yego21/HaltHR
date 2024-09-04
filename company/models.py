from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField
# from employee.models import UserProfile


import os

def event_directory_path(instance, filename):
    event_name = instance.title
    filename = f'{event_name}.jpg'
    return os.path.join('events/', event_name, filename)
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
    image1 = models.ImageField(upload_to=event_directory_path, default='events/event_1.jpg')
    # image2 = models.ImageField(upload_to=event_directory_path, blank=True)


    def __str__(self):
        return self.title


class Event_Media(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='events/')  # Set a generic path
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only do this if the object is being created (not updated)
            if self.media_type == 'photo':
                self.file.name = os.path.join('images/', self.file.name)
            elif self.media_type == 'video':
                self.file.name = os.path.join('videos/', self.file.name)
        super(Event_Media, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type.capitalize()} {self.id}"

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title









