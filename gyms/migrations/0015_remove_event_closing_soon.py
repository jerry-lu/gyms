# Generated by Django 2.2.4 on 2019-09-26 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0014_auto_20190926_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='closing_soon',
        ),
    ]
