
from django.urls import path

from .views import ClientProfileView

urlpatterns = [
    path('client/profile', ClientProfileView.as_view()),
]
