# Generated by Django 5.0.7 on 2024-09-09 01:30

import company.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_remove_event_image2_event_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_media',
            name='file',
            field=models.FileField(upload_to=company.models.event_files_directory_path),
        ),
        migrations.AlterField(
            model_name='event_media',
            name='media_type',
            field=models.CharField(choices=[('photo', 'Photo'), ('video', 'Video')], max_length=50),
        ),
    ]
