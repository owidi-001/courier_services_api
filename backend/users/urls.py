from django.urls import path
from .views import (RegisterUser, UserLogin, UpdatePasswordView, ForgotPasswordView, CustomerProfileView,
                    DriverProfileView)

from django.contrib.auth.views import LogoutView
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Auth user
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

    path("auth/update-password/", UpdatePasswordView.as_view(), name="password_update"),
    path("auth/reset/<uidb64>/<token>/", ForgotPasswordView.as_view(), name="reset"),

    # customer
    path('customer/profile/', CustomerProfileView.as_view()),

    # driver
    path('driver/profile/', DriverProfileView.as_view()),
]
