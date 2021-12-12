from rest_framework import serializers
from users.models import *
from shipment.models import *


# USERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["national_id", "phone_number", "first_name", "last_name", "email"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["name"]


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ["name"]


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    street = StreetSerializer()

    class Meta:
        model = Address
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = UserAddress
        fields = ["address", ]


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ["id", "user", "profile_image",
                  "phone_number", "dl_number", "national_id_number", "gender"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "profile_image", "phone_number"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """
    email = serializers.EmailField(required=True)


class NewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    new_password = serializers.CharField()
    short_code = serializers.IntegerField()


# SHIPMENT
class CargoSerializer(serializers.ModelSerializer):
    origin = CitySerializer()
    destination = CitySerializer()

    class Meta:
        model = Cargo
        fields = ["owner", "size", "sensitivity", "origin", "destination"]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["vehicle_registration_number", "carrier_type", "carrier_capacity", "model"]


class ShipmentSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer()
    driver = DriverSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = Shipment
        fields = ["__all__"]


class BookingSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer()
    customer = CustomerProfileSerializer()

    class Meta:
        model = CustomerBooking
        fields = "__all__"
