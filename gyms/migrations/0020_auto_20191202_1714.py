# Generated by Django 3.0 on 2019-12-02 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0019_auto_20190926_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]