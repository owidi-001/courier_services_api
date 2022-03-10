# Generated by Django 4.0 on 2022-03-08 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0012_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(auto_created=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('P', 'Pending'), ('C', 'Canceled'), ('F', 'fulfilled')], db_index=True, default='P', max_length=1),
        ),
    ]