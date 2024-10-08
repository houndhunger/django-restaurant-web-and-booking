# Generated by Django 4.2.15 on 2024-09-09 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_reservation_has_bench_seating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='has_bench_seating',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'Yes'), (2, 'No')], default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='has_disabled_access',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'Yes'), (2, 'No')], default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='is_outside',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'Yes'), (2, 'No')], default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='is_quiet',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'Yes'), (2, 'No')], default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='preference',
            field=models.IntegerField(choices=[(0, 'No Preference'), (1, 'Yes'), (2, 'No')], default=0),
        ),
    ]
