# Generated by Django 3.2 on 2021-09-08 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0006_auto_20210908_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendant',
            name='day',
            field=models.CharField(choices=[('day1', 'Day 1'), ('day2', 'Day 2'), ('day3', 'Day 3'), ('day4', 'Day 4'), ('day5', 'Day 5'), ('day6', 'Day 6'), ('day7', 'Day 7')], default='day1', max_length=5),
        ),
    ]
