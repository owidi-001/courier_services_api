# Generated by Django 4.0 on 2022-01-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0003_shipment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customershipment',
            name='confirmed',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='charge_rate',
            field=models.DecimalField(decimal_places=2, default=1000, help_text='The price a driver charges per km in KSH', max_digits=10),
            preserve_default=False,
        ),
    ]
