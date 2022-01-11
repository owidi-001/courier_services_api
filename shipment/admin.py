from django.contrib import admin
from .models import Cargo, Location,  Vehicle, Shipment, CustomerShipment, Feedback


class CargoAdmin(admin.ModelAdmin):
    list_display = ["owner", "size", "nature"]


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["cargo", "vehicle", "origin", "destination", "status","shipment_date"]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_registration_number", "model"]


class CustomerShipmentAdmin(admin.ModelAdmin):
    list_display = ["customer", "shipment"]


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Location)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(CustomerShipment, CustomerShipmentAdmin)
admin.site.register(Feedback)
