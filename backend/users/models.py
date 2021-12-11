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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.email}"


'''
generate authentication  token after a user has been created and send him/her an email
'''


@receiver(post_save, sender=User)
def create_auth_token(sender=None, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to=upload)
    phone_number = models.CharField(max_length=13)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class City(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    zip_code = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "addresses"

    def __str__(self) -> str:
        return f"{self.zip_code} {self.street} {self.city}, Kenya"


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="user_address")

    class Meta:
        unique_together = (("user", "address"),)
        db_table = "user_addresses"

    def __str__(self) -> str:
        return f"{self.user} - {self.address}"


# Driver
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to=upload)
    phone_number = models.CharField(max_length=13)
    gender = models.CharField(max_length=1, choices=(
        ("M", "Male"), ("F", "Female")
    ))
    dl_number = models.CharField(max_length=10, unique=True)  # license No
    national_id_number = models.CharField(max_length=8, unique=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_token = models.IntegerField(null=True)
    reset_token = models.CharField(max_length=100)