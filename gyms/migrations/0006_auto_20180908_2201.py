# Generated by Django 2.1.1 on 2018-09-09 02:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0005_auto_20180908_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
