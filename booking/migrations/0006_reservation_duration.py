# Generated by Django 4.2.15 on 2024-09-08 22:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_reservation_guest_count_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
    ]
