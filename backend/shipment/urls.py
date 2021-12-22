from django.urls import path
from .views import ShipmentView, DriverShipmentView, FeedbackView, customer_support

urlpatterns = [
    # SHIPMENT
    path("shipments/", ShipmentView.as_view(), name="shipments"),
    # profile shipment details
    path('profile/driver/<int:id>/', DriverShipmentView.as_view()),  # Driver list of shipments
    # Others
    path('support/', customer_support, name="support"),
    path('feedback/', FeedbackView.as_view()),

]
