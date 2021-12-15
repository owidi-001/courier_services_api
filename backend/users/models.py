from django.db import models
from django.contrib.auth.models import AbstractUser

# Generates auth token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail
from threading import Thread

# local modules
from .managers import UserManager


def upload(instance, filename):
    return f"images/{instance.user.id}/{filename}"


class EmailThead(Thread):
    def __init__(self, email_to, message):
        super().__init__()
        self.email_to = email_to
        self.message = message

    def run(self):
        send_mail("subject", self.message, settings.EMAIL_HOST_USER, self.email_to,
                  fail_silently=True, html_message=self.message)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=8, null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=13, null=False, blank=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["national_id", "phone_number"]
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"


# generate authentication  token after a user has been created and send him/her an email
@receiver(post_save, sender=User)
def create_auth_token(sender=None, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to=upload)

    def __str__(self) -> str:
        return f"{self.user.email}"

    def get_name(self):
        return f"{self.user.name}"


# Driver
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to=upload)
    gender = models.CharField(max_length=1, choices=(
        ("M", "Male"), ("F", "Female")
    ))
    dl_number = models.CharField(max_length=10, unique=True)  # license No

    def __str__(self) -> str:
        return f"{self.user.email}: {self.dl_number}"


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_token = models.IntegerField(null=True)
    reset_token = models.CharField(max_length=100)
