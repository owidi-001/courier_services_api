from django.urls import path


from .views import ClientProfileView, VehicleListView

urlpatterns = [
    path("client/profile/", ClientProfileView.as_view()),
    path("client/vehicle/", VehicleListView.as_view()),
]
