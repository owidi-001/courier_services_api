# Generated by Django 4.0 on 2022-02-02 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_driver_is_active_alter_driver_dl_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('P', 'Prefer Not To Say')], max_length=1),
        ),
    ]
