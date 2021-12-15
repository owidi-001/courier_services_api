from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from .app_notifications import send_multicast
from users.models import Customer, EmailThead,Driver


class Cargo(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    size = models.IntegerField(default=1)
    nature = models.CharField(max_length=100, help_text="How fragile is your cargo",
                              choices=(("F", "fragile"), ("NF", "Not Fragile"), ("HWC", "Handle with care")))
    description = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Add name or a brief description of your package eg Animal,Building tools etc")

    def __str__(self) -> str:
        return f"{self.owner} Approximately {self.size} units"


class Vehicle(models.Model):
    carrier_type = models.CharField(max_length=100, help_text="vehicle carriage type",
                                    choices=(("L", "Lorry"), ("P", "Pickup"), ("B", "MotorBike")))
    carrier_capacity = models.CharField(max_length=100, help_text="vehicle carrying capacity",
                                        choices=(("L", "Large"), ("M", "Medium"), ("S", "Small")))
    vehicle_registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100, help_text="vehicle model type")

    def __str__(self) -> str:
        return f"{self.vehicle_registration_number} - {self.carrier_capacity} {self.carrier_type} "


class Location(models.Model):
    long_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)


class Origin(Location):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Destination(Location):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    origin = models.ForeignKey(Origin, on_delete=models.PROTECT)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=(
        ("C", "canceled"), ("F", "fulfilled"), ("A", "active")
    ), default="A")
    shipment_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    carriage = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.status}"


class CustomerShipment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("shipment", "customer")

    def __str__(self) -> str:
        return f"{self.shipment.state} - {self.customer.name}"


# send notification when the shipment is done
@receiver(post_save, sender=CustomerShipment)
def send_customer_notification(sender=None, instance=None, created=False, **kwargs):
    try:
        if instance.status == "A":
            clients = CustomerShipment.objects.filter(
                shipment=instance.shipment, status="A")

            # push notification
            message = "The cargo arrived at their destination, you will receive a confirmation call."
            # email notification
            EmailThead([item.customer.email for item in clients] +
                       ["admin@gmail.com"], message)

    except:
        pass


class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    shipment = models.OneToOneField(CustomerShipment)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)

# class DriverPayment(models.Model):
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     amount = models.IntegerField(default=0)
