# Generated by Django 3.2 on 2021-09-06 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendant',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='eventdetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='year',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
