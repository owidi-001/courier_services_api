# Generated by Django 4.0 on 2022-02-02 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
        ('shipment', '0009_alter_customershipment_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='driver.driver'),
        ),
    ]