# Generated by Django 3.2 on 2022-11-08 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0009_alter_year_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendant',
            unique_together={('eventdetail', 'name', 'day', 'phone_number', 'level')},
        ),
    ]
