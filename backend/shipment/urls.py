from django.urls import path
from .views import ShipmentView, CustomerShipmentView, DriverShipmentView, FeedbackView, customer_support

urlpatterns = [
    # SHIPMENT
    path("shipments/", ShipmentView.as_view(), name="shipments"),
    path("customer/<int:id>/shipments/", CustomerShipmentView.as_view()),  # customer id the path ie <int:id>/shipments

    path('driver/<int:id>/shipments/', DriverShipmentView.as_view()),  # Driver list of shipments

    path('support/', customer_support),
    path('feedback/', FeedbackView.as_view()),

]
