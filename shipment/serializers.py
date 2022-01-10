
from django.db.models import fields

from rest_framework import serializers
from .models import Cargo, Location, Vehicle, Shipment, CustomerShipment,User

from users.serializers import UserSerializer, DriverSerializer


# SHIPMENT
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ["size", "nature"]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["vehicle_registration_number"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "lng", "lat", "name", "city", "street", "zip_code", "street_number",
        ]


class ShipmentSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer()
    origin = LocationSerializer()
    destination = LocationSerializer()

    class Meta:
        model = Shipment
        fields = ["cargo", "origin", "destination",
                  "vehicle", "price", "status", "shipment_date"]

    def save(self, request)->Shipment:
        cargo = Cargo.objects.get_or_create(**self.validated_data["cargo"],owner=request.user)
        origin = Location.objects.get_or_create(
            **self.validated_data["origin"])
        destination = Location.objects.get_or_create(
            **self.validated_data["destination"])
            
        print(cargo, origin, destination)


class CustomerShipmentSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer()
    customer = UserSerializer()

    class Meta:
        model = CustomerShipment
        fields = "__all__"
