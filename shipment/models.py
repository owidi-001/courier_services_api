from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from driver.models import Driver, Vehicle
from shipment.utils import coordinateDistance, randomString
from users.models import User
from users.views import EmailThead


class Size(models.TextChoices):
    Large = "L"
    Small = "S"
    Medium = "M"


class Cargo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(
        choices=Size.choices,
        max_length=1,
    )
    nature = models.CharField(
        max_length=2,
        help_text="What's the nature of your cargo?",
        choices=(
            ("F", "fragile"),
            ("NF", "Not Fragile"),
        ),
    )

    class Meta:
        verbose_name_plural = "cargo"

    def __str__(self) -> str:
        return f"{self.size},{self.nature} package. Owned by {self.owner}"


# Shipment pick point
class Location(models.Model):
    lng = models.FloatField(
        null=True,
        blank=True,
    )
    lat = models.FloatField(
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "location"

    def __str__(self):
        return f"{self.street},{self.city},Kenya"


class Shipment(models.Model):
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
    )
    origin = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="pickup",
    )
    destination = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="dropoff",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        max_length=1,
        choices=(
            ("A", "Active"),
            ("P", "Pending"),
            ("C", "Canceled"),
            ("F", "fulfilled"),
        ),
        default="P",
    )
    shipment_date = models.DateTimeField(
        auto_now_add=True,
    )
    price = models.IntegerField()
    rating = models.FloatField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.origin} - {self.destination} by {self.vehicle}"

    @property
    def date(self):
        # date_time = datetime.fromisoformat(self.shipment_date)
        return self.shipment_date.strftime("%d %B, %Y")

    @property
    def distance(self) -> float:
        return self.price / self.vehicle.charge_rate

    def save(self, distance=None, *args, **kwargs):
        if self.id is None:
            # perform this operation only when the object is created for the first time
            # distance will help to calcute  price
            try:
                distance_ = distance or coordinateDistance(
                    self.origin.lat,
                    self.origin.lng,
                    self.destination.lat,
                    self.destination.lng,
                )
            except:
                raise ValidationError(
                    """
                Calculated distance between origin and destination in km 
                if the value is left empty, origin lat, lng
                and destination origin lat,lng must be provided
                            
                    """
                )
            # calculate price based on the distance and vehicle.charge_rate per km
            self.price = distance_ * self.vehicle.charge_rate

        super().save(*args, **kwargs)


class CustomerShipment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if self.id is None:
            # generate order number  only once,
            #  when the object is created for the first time
            self.order_number = randomString()
        super().save(args, kwargs)

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
                shipment=instance.shipment, status="F"
            )

            message = "The cargo arrived at their destination."
            # email notification
            EmailThead(
                [item.customer.email for item in clients] + ["admin@gmail.com"], message
            )

    except:
        pass


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, default=None)
    message = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.user}: {self.message}"
