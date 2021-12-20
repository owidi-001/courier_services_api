from django.urls import path
from .views import ShipmentView, CustomerShipmentView, DriverShipmentView, FeedbackView, customer_support

urlpatterns = [
    # SHIPMENT
    path("shipments/", ShipmentView.as_view(), name="shipments"),
    # profile shipment details
    path("profile/customer/<int:id>/", CustomerShipmentView.as_view()),  # customer id the path ie <int:id>/shipments
    path('profile/driver/<int:id>/', DriverShipmentView.as_view()),  # Driver list of shipments
    # Others
    path('support/', customer_support),
    path('feedback/', FeedbackView.as_view()),

]
