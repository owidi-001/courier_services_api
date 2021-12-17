from abc import ABC

from rest_framework import serializers
from shipment.models import Cargo,Vehicle,Shipment,CustomerShipment

from users.serializers import CustomerSerializer,DriverSerializer


# SHIPMENT
class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = ["owner", "size", "nature"]


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


class CustomerShipmentSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = CustomerShipment
        fields = "__all__"
