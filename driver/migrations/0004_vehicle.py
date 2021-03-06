# Generated by Django 4.0 on 2022-02-02 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_alter_driver_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrier_type', models.CharField(choices=[('L', 'Lorry'), ('P', 'Pickup'), ('B', 'MotorBike')], help_text='vehicle carriage type', max_length=100)),
                ('carrier_capacity', models.CharField(choices=[('L', 'Large'), ('S', 'Small'), ('M', 'Medium')], help_text='Approximate vehicle carrying capacity', max_length=100)),
                ('vehicle_registration_number', models.CharField(max_length=20, unique=True)),
                ('charge_rate', models.FloatField(help_text='The price a driver charges per km in KSH')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='driver.driver')),
            ],
            options={
                'verbose_name_plural': 'Vehicle',
            },
        ),
    ]
