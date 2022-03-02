from wsgiref.validate import validator
from rest_framework import serializers

from driver.models import Driver, Vehicle
from users.serializers import UserSerializer


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ["user", "dl_number", "gender", "is_active"]


class VehicleSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = Vehicle
        fields = ["carrier_type", "driver", "carrier_capacity",
                  "vehicle_registration_number", "charge_rate", "id"]
