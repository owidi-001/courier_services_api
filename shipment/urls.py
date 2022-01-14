from django.urls import path
from .views import (
    ShipmentView,
    DriverShipmentRequestView,
    FeedbackView,
    VehicleView,
    customer_support,
)

urlpatterns = [
    # SHIPMENT
    path("shipments/", ShipmentView.as_view(), name="shipments"),
    path("vehicle/", VehicleView.as_view(), name="vehicle"),
    # profile shipment details
    path(
        "driver/shipment/", DriverShipmentRequestView.as_view()
    ),  # Driver list of shipments
    # Others
    path("support/", customer_support, name="support"),
    path("feedback/", FeedbackView.as_view()),
]
