# Generated by Django 5.0.7 on 2024-08-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image1',
            field=models.ImageField(default='events/event_1.jpg', upload_to='events/%m/%d/%Y/'),
        ),
        migrations.AddField(
            model_name='event',
            name='image2',
            field=models.ImageField(blank=True, upload_to='events/%m/%d/%Y/'),
        ),
    ]
