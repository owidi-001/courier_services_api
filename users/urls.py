from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (RegisterUser, UserLogin, UpdatePasswordView,
                    DriverProfileView, RegisterDriver, UserProfileView, ResetPasswordView)

urlpatterns = [
    # Auth user
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", UserLogin.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

    # create driver
    path("auth/driver/", RegisterDriver.as_view(), name="driver_register"),

    path("auth/update-password/", UpdatePasswordView.as_view(), name="password_update"),
    path("auth/reset/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset"),

    # Profiles
    path('profile/', UserProfileView.as_view()),
    path('profile/driver/', DriverProfileView.as_view()),

]
