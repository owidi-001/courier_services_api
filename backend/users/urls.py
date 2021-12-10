from django.urls import path
from .views import (CustomerProfileView,customer_suport, RegisterCustomer, ChangePasswordView,FeedbackView,
                      UserAddressView,  CustomerBookingView, UserLogin, ForgotPasswordView)
# from rest_framework.documentation import include_docs_urls

from backend.api.driver_views import DriverProfileView, DriverShipment


urlpatterns = [

    # Auth
    path("auth/login/", UserLogin.as_view()),
    path("auth/change-password/", ChangePasswordView.as_view()),
    path("auth/customer/register/", RegisterCustomer.as_view()),
    path("auth/reset/", ForgotPasswordView.as_view()),

    # Customer
    path("customer/booking/", CustomerBookingView.as_view()),
    path('customer/profile/', CustomerProfileView.as_view()),
    # Driver
    path('driver/profile/', DriverProfileView.as_view()),
    path('driver/shipment/', DriverShipment.as_view()),
    path('support/', customer_suport),
    
    # Address
    path("address/", UserAddressView.as_view()),
    # Feedback
    path('feedback/', FeedbackView.as_view()),
]