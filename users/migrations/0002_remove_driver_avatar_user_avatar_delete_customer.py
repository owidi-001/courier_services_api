# Generated by Django 4.0 on 2021-12-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='avatar',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]