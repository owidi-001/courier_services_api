from django.contrib import admin
from .models import *


class DriverAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "dl_number"]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "phone_number"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name",
                    "email", "date_joined", "is_staff"]
    search_fields = ["first_name", "last_name", "email"]


class AddressAdmin(admin.ModelAdmin):
    list_display = ("street", "city", "zip_code")


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address")


admin.site.register(Driver, DriverAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserAddress, UserAddressAdmin)