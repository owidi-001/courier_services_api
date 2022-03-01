from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

# users
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# driver_views
from driver.driver_doc_schema import DriverSchema
from driver.forms import DriverProfileUpdateForm
from driver.models import Driver
from driver.serializers import DriverSerializer, VehicleSerializer

# Create your views here.
from shipment.models import Vehicle
from users.models import User


class DriverProfileView(APIView):
    """
    Api endpoint for driver profile. Works the same as customers
    """

    schema = DriverSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def driver_active(self, request):
        """
        Activate driver when license and vehicle are provided
        """
        driver = get_object_or_404(Driver, user=request.user)
        print(driver)
        print(type(driver), "Driver object type")

        vehicles = Vehicle.objects.filter(driver=driver)

        if driver.dl_number is not None and len(vehicles) != 0 and not driver.is_active:
            driver.is_active = True
            driver.save()

        return driver

    def get(self, request):
        """
        > Returns driver profile details
        """
        driver = self.driver_active(request)
        return Response(DriverSerializer(driver).data)

    def put(self, request):
        """
        The driver updates profile details
        """

        form = DriverProfileUpdateForm(request.data)
        if form.is_valid():
            user = request.user
            driver = get_object_or_404(Driver, user=user)
            if form.cleaned_data.get("email"):
                user.email = form.cleaned_data["email"]
                user.save()
            if form.cleaned_data.get("phone_number"):
                driver.phone_number = form.cleaned_data["phone_number"]
            if form.cleaned_data.get("profile_image"):
                driver.profile_image = form.cleaned_data["profile_image"]
            driver.save()
            return Response(DriverSerializer(driver).data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """update driver avatar"""
        if request.FILES:
            profile = User.objects.get(user=request.user)
            profile.avatar = request.FILES[0]
            profile.save()
            return Response(
                {"message": "avatar updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "invalid image"}, status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name="dispatch")
class VehicleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
        Vehicle object manipulation views
    """

    def get(self, request):
        """
        Returns all vehicle belonging to a driver
        """
        query = Vehicle.objects.filter(driver__user=request.user)

        return Response(
            VehicleSerializer(query, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Driver add a new vehicle
        """

        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.driver = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Driver updates his/her vehicle
        """

        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Driver removes his/her vehicle
        """
        vehicle = self.get_object(pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
