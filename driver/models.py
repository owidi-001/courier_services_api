from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from backend import settings
from users.models import User


class Size(models.TextChoices):
    Large = "L"
    Small = "S"
    Medium = "M"


class Driver(models.Model):
    GENDER = (
        ("M", "Male"), ("F", "Female"), ("P", "Prefer Not To Say")
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    dl_number = models.CharField(max_length=10, unique=True, null=True,)
    gender = models.CharField(max_length=1, choices=GENDER, default="P",)
    # Driver becomes active by adding vehicle and license
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name_plural = "Drivers"


def create_driver_profile(sender, instance, created, **kwargs):
    if created:
        driver = Driver.objects.create(user=instance)
        driver.gender = "P"
        driver.save()


post_save.connect(create_driver_profile, sender=User)


class Vehicle(models.Model):
    # One driver can own/drive many vehicles
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, db_index=True)
    carrier_type = models.CharField(
        max_length=100,
        help_text="vehicle carriage type",
        choices=(
            ("L", "Lorry"),
            ("P", "Pickup"),
            ("B", "MotorBike"),
        ),
    )
    carrier_capacity = models.CharField(
        max_length=100,
        help_text="Approximate vehicle carrying capacity",
        choices=Size.choices,
    )
    vehicle_registration_number = models.CharField(
        max_length=20,
        unique=True,
    )
    charge_rate = models.FloatField(
        help_text="The price a driver charges per km in KSH",
    )

    class Meta:
        verbose_name_plural = "Vehicle"

    def __str__(self) -> str:
        return f"{self.vehicle_registration_number}"
