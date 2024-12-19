# Generated by Django 5.0.7 on 2024-12-19 03:35

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_company_about_image_company_description_career'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_media',
            name='video_file',
            field=cloudinary.models.CloudinaryField(blank=True, default='events/event_1.jpg', max_length=255, null=True, verbose_name='video'),
        ),
        migrations.AlterField(
            model_name='event_media',
            name='file',
            field=cloudinary.models.CloudinaryField(blank=True, default='events/event_1.jpg', max_length=255, null=True, verbose_name='media'),
        ),
    ]
