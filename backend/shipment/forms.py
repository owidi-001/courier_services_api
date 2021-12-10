from django import forms
from .models import Shipment


class BookingForm(forms.Form):
    class Meta:
        model = Shipment
        fields = ['__all__']
