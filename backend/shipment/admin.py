from django.contrib import admin
from .models import *


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["cargo", "vehicle",
                    "driver", "departure", "arrival", "status"]


class CargoAdmin(admin.ModelAdmin):
    list_display = ["origin", "destination"]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_registration_number", "model"]


class CustomerBookingAdmin(admin.ModelAdmin):
    list_display = ["customer", "status"]


admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CustomerBooking, CustomerBookingAdmin)
admin.site.register(Feedback)
