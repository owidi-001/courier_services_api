from django.contrib import admin

# Register your models here.
from driver.models import Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = ["user", "dl_number", "gender"]


admin.site.register(Driver, DriverAdmin)
