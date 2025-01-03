from django.db import models
from django.contrib.auth.models import User
from django.utils.translation.template import blankout
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from moviepy.editor import VideoFileClip
import os
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill
from django.core.files import File
from django.conf import settings
from django.db.models import JSONField
from django.utils import timezone
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy
from cloudinary.utils import cloudinary_url


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(80, 80)]
    format = 'JPEG'
    options = {'quality': 60}

#FOR LOCAL SAVING SETTINGS ENABLE THIS
# def hero_directory_path(instance, filename):
#     hero_image_name = instance.name
#     # Extract the original file extension
#     original_extension = os.path.splitext(filename)[1]  # Get the file extension (e.g., .jpg, .jpeg, .png)
#     filename = f'{hero_image_name}{original_extension}'  # Use the original extension
#     return os.path.join(settings.MEDIA_ROOT, 'hero', hero_image_name, filename)
#
# def about_directory_path(instance, filename):
#     about_image_name = instance.name
#     # Extract the original file extension
#     original_extension = os.path.splitext(filename)[1]  # Get the file extension (e.g., .jpg, .jpeg, .png)
#     filename = f'{about_image_name}{original_extension}'  # Use the original extension
#     return os.path.join(settings.MEDIA_ROOT, 'about', about_image_name, filename)
#
# def event_directory_path(instance, filename):
#     event_name = instance.title
#     filename = f'{event_name}.jpg'
#     return os.path.join(settings.MEDIA_ROOT, 'events',  f'{event_name}', filename)
#
#
# # Create your models here.
# def event_files_directory_path(instance, filename):
#     event_name = instance.event
#     get_ext = instance.file.name.split('.')
#     if instance.caption:
#         filename = f'{instance.caption}.{get_ext[-1]}'
#     else:
#         filename = instance.file.name
#
#     if instance.media_type == 'photo':
#         return os.path.join(settings.MEDIA_ROOT, 'events_media', f'{event_name}', 'images', filename)
#     elif instance.media_type == 'video':
#         return os.path.join(settings.MEDIA_ROOT, 'events_media',  f'{event_name}', 'videos', filename)
#
# def snap_thumbnail(video_path, thumbnail_path, time_frame=5):
#     with VideoFileClip(video_path) as video:
#         frame = video.get_frame(time_frame)
#         thumbnail = video.save_frame(thumbnail_path, t=time_frame)
#     return thumbnail
#
# def create_video_thumbnail(instance):
#     if instance.media_type == 'video':
#         video_path = instance.file.path
#         thumbnail_path = os.path.join('media/CACHE/', f'{instance.id}_thumbnail.jpg')
#         snap_thumbnail(video_path, thumbnail_path)
#
#         with open(thumbnail_path, 'rb') as f:
#             source_file = File(f)
#             image_generator = Thumbnail(source=source_file)
#             result = image_generator.generate()
#
#             # Save the result to a new path
#             thumbnail_dir = os.path.join('media/CACHE/thumbnails/')
#             final_thumbnail_path = os.path.join('media/CACHE/thumbnails/', f'{instance.id}_thumbnail.jpg')
#             os.makedirs(thumbnail_dir, exist_ok=True)
#             with open(final_thumbnail_path, 'wb') as dest:
#                 dest.write(result.read())
#
#         return final_thumbnail_path



#FOR CLOUDINARY SETTINGS ENABLE THIS
def hero_directory_path(instance, filename):
    hero_image_name = instance.name
    # Extract the original file extension
    original_extension = os.path.splitext(filename)[1]  # Get the file extension (e.g., .jpg, .jpeg, .png)
    filename = f'hero/{hero_image_name}{original_extension}'  # Use the original extension
    return filename

def about_directory_path(instance, filename):
    about_image_name = instance.name
    # Extract the original file extension
    original_extension = os.path.splitext(filename)[1]  # Get the file extension (e.g., .jpg, .jpeg, .png)
    filename = f'about/{about_image_name}{original_extension}'  # Use the original extension
    return filename

def event_directory_path(instance, filename):
    event_name = instance.title
    filename = f'events/{event_name}/{event_name}.jpg'
    return filename


# Create your models here.
def event_files_directory_path(instance):
    event_name = instance.event
    filename = instance.caption
    # get_ext = instance.file.name.split('.')
    # if instance.caption:
    #     filename = f'{instance.caption}.{get_ext[-1]}'
    # else:
    #     filename = instance.file.name

    if instance.media_type == 'photo':
        return f'events_media/{event_name}/images/{filename}.png'
    elif instance.media_type == 'video':
        return f'events_media/{event_name}/videos/{filename}'

def snap_thumbnail(video_path, thumbnail_path, time_frame=5):
    with VideoFileClip(video_path) as video:
        frame = video.get_frame(time_frame)
        thumbnail = video.save_frame(thumbnail_path, t=time_frame)
    return thumbnail

def create_video_thumbnail(instance):
    if instance.media_type == 'video':
        video_path = instance.file.path
        thumbnail_path = f'media/CACHE/{instance.id}_thumbnail.jpg'
        snap_thumbnail(video_path, thumbnail_path)

        with open(thumbnail_path, 'rb') as f:
            source_file = File(f)
            image_generator = Thumbnail(source=source_file)
            result = image_generator.generate()

            # Save the result to a new path
            thumbnail_dir = f'/CACHE/thumbnails/'
            final_thumbnail_path = f'/CACHE/thumbnails/{instance.id}_thumbnail.jpg'
            os.makedirs(thumbnail_dir, exist_ok=True)
            with open(final_thumbnail_path, 'wb') as dest:
                dest.write(result.read())

        return final_thumbnail_path





class Company(models.Model):
    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)  # Assuming ID 1 is your singleton
        return obj
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    about_image = models.ImageField(upload_to=about_directory_path, null=True, blank=True)
    hero_image1 = models.ImageField(upload_to=hero_directory_path, null=True, blank=True)
    hero_image2 = models.ImageField(upload_to=hero_directory_path, null=True, blank=True)
    hero_image3 = models.ImageField(upload_to=hero_directory_path, null=True, blank=True)
    hero_image4 = models.ImageField(upload_to=hero_directory_path, null=True, blank=True)
    hero_image5 = models.ImageField(upload_to=hero_directory_path, null=True, blank=True)


    def __str__(self):
        return self.name


class Career(models.Model):

    JOB_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CON', 'Contract'),
        ('INT', 'Internship'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, )
    job_title = models.CharField(max_length=255)
    job_type = models.CharField(max_length=3, choices=JOB_TYPES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience_required = models.CharField(max_length=255)
    qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    posting_date = models.DateField(auto_now_add=True, null=True, blank=True)
    application_link = models.URLField(null=True, blank=True)
    application_email = models.EmailField(null=True, blank=True)
    employment_status = models.BooleanField(default=True)  # True = Open, False = Closed
    work_hours = models.CharField(max_length=50, null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    application_instructions = models.TextField(null=True, blank=True)
    remote_option = models.BooleanField(default=False)

    def __str__(self):
        return self.job_title


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, )
    department_head = models.ForeignKey('employee.UserProfile', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='head_of_departments')

    def get_members(self):
        from employee.models import UserProfile
        return UserProfile.objects.filter(department=self)

    get_members.short_description = 'Members'

    # my_list = ArrayField(models.CharField(max_length=100), blank=True, default=member_list)
    def __str__(self):
        return self.name





class Event(models.Model):
    title = models.CharField(max_length=255)

    EVENT_TYPE_CHOICES = [
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('team_building', 'Team Building'),
        ('product_launch', 'Product Launch'),
        ('corporate_party', 'Corporate Party'),
        ('networking', 'Networking Event'),
        ('board_meeting', 'Board Meeting'),
        ('training', 'Training Session'),
        ('community_service', 'Community Service'),
        ('fundraiser', 'Fundraiser'),
        ('virtual_event', 'Virtual Event'),
        ('award_ceremony', 'Award Ceremony'),
        ('charity_event', 'Charity Event'),
        ('clean_up_drive', 'Clean-up Drive'),
        ('town_hall', 'Town Hall Meeting'),
        ('retreat', 'Retreat'),
        ('panel_discussion', 'Panel Discussion'),
        ('general_meeting', 'General Meeting'),
        ('client_meeting', 'Client Meeting'),
    ]
    category = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default="", blank=True)
    description = models.TextField()


    # Update to include time in the JSON field
    # event_dates = JSONField(default=list, blank=True)

    location = models.CharField(max_length=255)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to=event_directory_path, default='events/event_1.jpg')

    def __str__(self):
        return self.title

class Event_Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.date)



class Event_Media(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    # file = models.FileField(upload_to=event_files_directory_path)  # Set a generic path
    file = CloudinaryField('media', folder=event_files_directory_path,  blank=True, null=True, default='events/event_1.jpg')

    def get_thumbnail_url(self, height=150, width=150):
        return self.file.build_url(height=height, width=width, crop='fill')
    # media_thumbnail = ImageSpecField(source='file', processors=[ResizeToFill(80, 70)], format='JPEG',
    #                                  options={'quality': 60})
    # Call the function to get the path for the thumbnail

    # Pass the generated path to a field or directly use it in the template
    video_media_thumbnail = create_video_thumbnail
    media_url = str(video_media_thumbnail)

    caption = models.CharField(max_length=255, blank=True, null=True)





    def delete(self, *args, **kwargs):
        # Check if the file exists
        if self.file:
            # Extract the public_id from the file field
            public_id = self.file.public_id
            if public_id:
                # Use Cloudinary's API to delete the file
                destroy(public_id)

        # Call the superclass's delete method
        super().delete(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     # Delete the file from the filesystem
    #     if self.file:
    #         if os.path.isfile(self.file.path):
    #             os.remove(self.file.path)
    #     # Call the superclass's delete method
    #     super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type.capitalize()} {self.id}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title




register.generator('company:thumbnail', Thumbnail)
