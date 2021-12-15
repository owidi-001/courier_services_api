from django.urls import path
from .views import (CustomerProfileView, customer_support, RegisterCustomer, UpdatePasswordView, FeedbackView,
                    UserAddressView, CustomerBookingView, UserLogin, ForgotPasswordView)
from .driver_views import DriverProfileView, DriverShipment

urlpatterns = [
    # USER
    path("auth/register/", RegisterCustomer.as_view()),  # DONE
    path("auth/login/", UserLogin.as_view()),  # DONE
    path("auth/change-password/", UpdatePasswordView.as_view()),  # DONE
    path("auth/reset_password/", ForgotPasswordView.as_view()),  # DONE
    path('customer_profile/', CustomerProfileView.as_view()), # DONE

    # SHIPMENT
    path("booking/", CustomerBookingView.as_view()),


    path('driver_profile/', DriverProfileView.as_view()),

    path("address/", UserAddressView.as_view()),

    path('shipment/', DriverShipment.as_view()),
    path('support/', customer_support),
    path('feedback/', FeedbackView.as_view()),

]
