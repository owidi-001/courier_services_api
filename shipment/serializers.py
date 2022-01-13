from typing_extensions import Required
from django.db.models import fields
from rest_framework import serializers
from .models import Cargo, Location, Vehicle, Shipment, CustomerShipment, User
from users.serializers import UserSerializer, DriverSerializer
from datetime import datetime


# SHIPMENT
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ["size", "nature"]


class VehicleSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["id"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "lng",
            "lat",
            "name",
            "city",
            "street",
        ]


class ShipmentSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer()
    origin = LocationSerializer()
    destination = LocationSerializer()
    distance = serializers.FloatField(required=False)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "cargo",
            "origin",
            "destination",
            "vehicle",
            "price",
            "status",
            "date",
            "distance",
        ]

        read_only_fields = ["date", "id"]

    def save(self, request) -> CustomerShipment:
        cargo, _ = Cargo.objects.get_or_create(
            **self.validated_data["cargo"], owner=request.user
        )
        origin, _ = Location.objects.get_or_create(**self.validated_data["origin"])
        destination, _ = Location.objects.get_or_create(
            **self.validated_data["destination"]
        )
        cargo.save()
        destination.save()
        origin.save()
        # TODO: work out price calculations
        shipment = Shipment(
            origin=origin,
            destination=destination,
            cargo=cargo,
            vehicle=self.validated_data["vehicle"],
        )
        shipment.save(
            distance=self.validated_data["distance"],
        )
        customer_shipment, _ = CustomerShipment.objects.get_or_create(
            shipment=shipment,
            customer=request.user,
        )
        customer_shipment.save()
        return customer_shipment


class CustomerShipmentSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer()
    customer = UserSerializer()

    class Meta:
        model = CustomerShipment
        fields = "__all__"
