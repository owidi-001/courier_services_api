# Generated by Django 4.0 on 2022-01-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0004_remove_customershipment_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='charge_rate',
            field=models.FloatField(help_text='The price a driver charges per km in KSH'),
        ),
    ]