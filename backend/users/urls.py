from django.urls import path
from .views import (RegisterUser, UserLogin, UpdatePasswordView, ForgotPasswordView, CustomerProfileView,
                    DriverProfileView)

from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    # Auth user
    path("auth/register/", RegisterUser.as_view()),
    path("auth/login/", UserLogin.as_view()),
    path("logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

    path("auth/change-password/", UpdatePasswordView.as_view()),
    path("auth/reset_password/", ForgotPasswordView.as_view()),

    # customer
    path('customer/profile/', CustomerProfileView.as_view()),

    # driver
    path('driver/profile/', DriverProfileView.as_view()),
]
