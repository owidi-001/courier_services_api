from django import forms
from .models import Shipment


class ShipmentForm(forms.Form):
    class Meta:
        model = Shipment
        fields = ["cargo", "origin", "destination", "vehicle"]
