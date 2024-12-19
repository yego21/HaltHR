# Generated by Django 5.0.7 on 2024-12-19 03:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_event_media_video_file_alter_event_media_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_media',
            name='video_file',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='video'),
        ),
    ]
