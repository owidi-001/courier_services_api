from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from .app_notifications import send_multicast
from users.models import Customer, City, Driver, EmailThead, User


class Vehicle(models.Model):
    carrier_type = models.CharField(max_length=100, help_text="vehicle carriage type",
                                    choices=(("L", "Lorry"), ("P", "Pickup"), ("B", "MotorBike")))
    carrier_capacity = models.CharField(max_length=100, help_text="vehicle carrying capacity",
                                        choices=(("L", "Large"), ("M", "Medium"), ("S", "Small")))
    vehicle_registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100, help_text="vehicle model type")

    def __str__(self) -> str:
        return f"{self.vehicle_registration_number} - {self.carrier_capacity} {self.carrier_type} "


class Cargo(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    size = models.IntegerField(default=1)
    sensitivity = models.CharField(max_length=100, help_text="How fragile is your cargo",
                                   choices=(("F", "fragile"), ("NF", "Not Fragile"), ("HWC", "Handle with care")))
    description = models.TextField(null=True, blank=True)
    origin = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="to")

    class Meta:
        unique_together = (("origin", "destination"),)

    def __str__(self) -> str:
        return f"{self.owner} From {self.origin} -> {self.destination}"


class Shipment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departure = models.DateTimeField(null=True, blank=True, default=timezone.now)
    arrival = models.DateTimeField(null=True, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    status = models.CharField(max_length=1, choices=(
        ("C", "canceled"), ("F", "fulfilled"), ("A", "active")
    ), default="A")

    def __str__(self) -> str:
        return f"{self.route.origin} - {self.route.destination} trip"


class CustomerBooking(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=(
        ("C", "canceled"), ("A", "active"), ("F", "fulfilled")
    ), default="A")

    class Meta:
        unique_together = ("shipment", "customer")

    def __str__(self) -> str:
        return f"{self.shipment} - {self.customer.user}"


# send notification when the shipment is done
@receiver(post_save, sender=CustomerBooking)
def send_user_notification(sender=None, instance=None, created=False, **kwargs):
    try:
        if instance.status == "A":
            clients = CustomerBooking.objects.filter(
                trip=instance.shipment, status="A")

            # push notification
            message = "The cargo arrived at their destination, you will receive a confirmation call."
            # email notification
            EmailThead([item.customer.email for item in clients] +
                       ["xxxyyyzzz@gmail.com"], message)

    except:
        pass


class DriverPayment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)
