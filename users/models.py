from multiprocessing.connection import Client
from django.contrib.auth.models import AbstractUser
from django.db import models
# Generates auth token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from courier_services_api.driver.models import Driver

# local modules
from .managers import UserManager


def upload(instance, filename):
    return f"media/{instance.user.id}/{filename}"


class User(AbstractUser):
    username = models.CharField(max_length=30, blank=False, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=13, null=False, blank=False, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='media/')
    is_driver = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"


"""
 generate authentication  token after a user has been created and send him/her an email
"""


def create_user(sender, instance, created, **kwargs):
    if created:
        auth_token = Token.objects.create(user=instance)
        client_profile = Client.objects.create(user=instance)
        driver_profile = Driver.objects.create(user=instance)

        client_profile.save()
        driver_profile.save()
        auth_token.save()


post_save.connect(create_user, sender=User)


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_token = models.IntegerField(null=True)
    reset_token = models.CharField(max_length=100)
