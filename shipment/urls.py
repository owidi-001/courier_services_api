from django.urls import path
from .views import (
    ShipmentView,
    DriverShipmentRequestView,
    FeedbackView,
    customer_support,
)

urlpatterns = [
    # SHIPMENT
    path("shipment/client", ShipmentView.as_view(), name="shipments"),
    path("shipment/driver", DriverShipmentRequestView.as_view()),  # Driver list of shipments

    # Others
    path("support/", customer_support, name="support"),
    path("feedback/", FeedbackView.as_view()),
]
