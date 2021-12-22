from django.contrib import admin
from .models import User, Customer, Driver


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email"]


class DriverAdmin(admin.ModelAdmin):
    list_display = ["user"]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(User)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Customer, CustomerAdmin)
