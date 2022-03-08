from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from backend import settings
from users.models import User


class Client(models.Model):
    GENDER = (
        ("M", "Male"), ("F", "Female"), ("P", "Prefer Not To Say")
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    gender = models.CharField(max_length=1, choices=GENDER)
    # Client becomes active if he/she has made a shipment
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user},{self.gender}"

    class Meta:
        verbose_name_plural = "Clients"


def create_user(sender, instance, created, **kwargs):
    if created:
        client_profile = Client.objects.create(user=instance)
        client_profile.save()


post_save.connect(create_user, sender=User)
