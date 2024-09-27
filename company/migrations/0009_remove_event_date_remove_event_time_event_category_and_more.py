# Generated by Django 5.0.7 on 2024-09-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_company_hero_image1_company_hero_image2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(blank=True, choices=[('seminar', 'Seminar'), ('conference', 'Conference'), ('workshop', 'Workshop'), ('team_building', 'Team Building'), ('product_launch', 'Product Launch'), ('corporate_party', 'Corporate Party'), ('networking', 'Networking Event'), ('board_meeting', 'Board Meeting'), ('training', 'Training Session'), ('community_service', 'Community Service'), ('fundraiser', 'Fundraiser'), ('virtual_event', 'Virtual Event'), ('award_ceremony', 'Award Ceremony'), ('charity_event', 'Charity Event'), ('clean_up_drive', 'Clean-up Drive'), ('town_hall', 'Town Hall Meeting'), ('retreat', 'Retreat'), ('panel_discussion', 'Panel Discussion'), ('general_meeting', 'General Meeting'), ('client_meeting', 'Client Meeting')], default='', max_length=50),
        ),
        migrations.AddField(
            model_name='event',
            name='event_dates',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
