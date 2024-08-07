# Generated by Django 5.0.7 on 2024-08-06 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_remove_department_member_list_and_more'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='department_head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_departments', to='employee.userprofile'),
        ),
    ]
