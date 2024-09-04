# Generated by Django 5.0.7 on 2024-08-28 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='contact',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.CharField(default='Member', max_length=50),
        ),
    ]