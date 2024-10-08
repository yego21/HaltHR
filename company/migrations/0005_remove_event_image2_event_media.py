# Generated by Django 5.0.7 on 2024-09-04 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_event_image1_alter_event_image2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image2',
        ),
        migrations.CreateModel(
            name='Event_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('photo', 'Photo'), ('video', 'Video')], max_length=10)),
                ('file', models.FileField(upload_to='events_media/')),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.event')),
            ],
        ),
    ]
