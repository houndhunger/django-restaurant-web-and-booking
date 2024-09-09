# Generated by Django 4.2.15 on 2024-09-09 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_alter_reservation_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='has_bench_seating',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'True'), (2, 'False')], default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='has_disabled_access',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'True'), (2, 'False')], default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_outside',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'True'), (2, 'False')], default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_quiet',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'True'), (2, 'False')], default=0),
        ),
    ]
