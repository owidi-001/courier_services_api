from django.urls import path

from driver.views import DriverProfileView,VehicleView

urlpatterns = [
    path('driver/profile', DriverProfileView.as_view()),
    path("driver/vehicle", VehicleView.as_view(), name="vehicle"),
]
