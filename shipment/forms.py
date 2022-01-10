from django import forms
from rest_framework import serializers

from .models import Shipment


class ShipmentForm(forms.Form):

    class Meta:
        model = Shipment
        fields = ["cargo", "origin", "destination", "vehicle", "price","status"]





