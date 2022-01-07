from django.contrib import admin
from .models import User, Driver


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "username"]


class DriverAdmin(admin.ModelAdmin):
    list_display = ["user", "dl_number", "gender"]


admin.site.register(User, UserAdmin)
admin.site.register(Driver, DriverAdmin)
