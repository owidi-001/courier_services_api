from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import Driver, User
from users.views import EmailThead


class Cargo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField(default=1)
    nature = models.CharField(max_length=100, help_text="What's the nature of your cargo?",
                              choices=(("F", "fragile"), ("NF", "Not Fragile")))

    class Meta:
        verbose_name_plural = "cargo"

    def __str__(self) -> str:
        return f"{self.size},{self.nature} package. Owned by {self.owner}"


# Shipment pick point
class Origin(models.Model):
    long_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        verbose_name_plural = "origin"

    def __str__(self):
        return f"Lat={self.lat_position},Lon={self.long_position}"


class Destination(models.Model):
    long_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        verbose_name_plural = "destination"

    def __str__(self):
        return f"Lat={self.lat_position},Lon={self.long_position}"


class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)  # One driver can own/drive many vehicles
    carrier_type = models.CharField(max_length=100, help_text="vehicle carriage type",
                                    choices=(("L", "Lorry"), ("P", "Pickup"), ("B", "MotorBike")))
    carrier_capacity = models.CharField(max_length=100, help_text="Approximate vehicle carrying capacity",
                                        choices=(("L", "Large"), ("M", "Medium"), ("S", "Small")))
    vehicle_registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100, help_text="vehicle model type")

    class Meta:
        verbose_name_plural = "Vehicle"

    def __str__(self) -> str:
        return f"{self.vehicle_registration_number}"


class Shipment(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    origin = models.ForeignKey(Origin, on_delete=models.PROTECT)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=1, choices=(
        ("A", "Active"),
        ("P", "Pending"),
        ("C", "Canceled"),
        ("F", "fulfilled")), default="P")
    shipment_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self) -> str:
        return f"{self.status}"


class CustomerShipment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("shipment", "customer")

    def __str__(self) -> str:
        return f"Owner: {self.customer} - Status: {self.shipment}"


# send notification when the shipment is done
@receiver(post_save, sender=CustomerShipment)
def send_customer_notification(sender=None, instance=None, created=False, **kwargs):
    try:
        if instance.status == "F":
            clients = CustomerShipment.objects.filter(
                shipment=instance.shipment, status="F")

            message = "The cargo arrived at their destination."
            # email notification
            EmailThead([item.customer.email for item in clients] +
                       ["admin@gmail.com"], message)

    except:
        pass


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)

    class Meta:
        verbose_name_plural = "Feedback"
