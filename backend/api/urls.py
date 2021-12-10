from django.urls import path
from .views import (CustomerProfileView, customer_support, RegisterCustomer, ChangePasswordView, FeedbackView,
                    UserAddressView, CustomerBookingView, UserLogin, ForgotPasswordView)
from .driver_views import DriverProfileView, DriverShipment


urlpatterns = [
    path("auth/register/", RegisterCustomer.as_view()),
    path("auth/login/", UserLogin.as_view()),
    path("address/", UserAddressView.as_view()),
    path('customer/profile/', CustomerProfileView.as_view()),
    path('driver/profile/', DriverProfileView.as_view()),
    path("auth/change-password/", ChangePasswordView.as_view()),
    path("auth/reset/", ForgotPasswordView.as_view()),
    path("customer/booking/", CustomerBookingView.as_view()),
    path('driver/trip/', DriverShipment.as_view()),
    path('support/', customer_support),
    path('feedback/', FeedbackView.as_view()),

]
