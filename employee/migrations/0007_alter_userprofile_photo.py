# Generated by Django 5.0.7 on 2024-12-19 03:35

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_userprofile_employment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dgee7iare/image/upload/v1731983114/photos/User_Four/123.png/tuochfczg3forerqgke5.jpg', max_length=255, verbose_name='image'),
        ),
    ]
