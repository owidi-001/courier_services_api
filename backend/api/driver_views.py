from users.forms import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Driver
from shipment.models import Shipment, CustomerBooking
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import DriverSerializer


class DriverProfileView(APIView):
    '''
     api endpoint for driver profile
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        > Returns driver profile details

        '''
        driver = get_object_or_404(Driver, user=request.user)
        return Response(DriverSerializer(driver).data)

    def put(self, request):
        '''
        updates driver details

        '''
        form = UserProfileUpdateForm(request.data)
        if form.is_valid():
            user = request.user
            driver = get_object_or_404(Driver, user=user)
            if form.cleaned_data.get("email"):
                user.email = form.cleaned_data["email"]
                user.save()
            if form.cleaned_data.get("phone_number"):
                driver.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data.get("profile_image"):
                driver.profile_image = form.cleaned_data["profile_image"]
            driver.save()
            return Response(DriverSerializer(driver).data, status=200)
        return Response(form.errors, status=400)


class DriverShipment(APIView):
    '''
     api endpoint for driver trip  
    '''

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        driver = get_object_or_404(Driver, user=request.user)
        shipment = Shipment.objects.filter(driver=driver)
        return Response(ShipmentSerializer(shipment,many=True).data)

    def post(self, request):
        '''
        return all customers who have booked
        '''
        shipment = get_object_or_404(Shipment, id=request.data.get("shipment_id"))
        customers = CustomerBooking.objects.filter(shipment=shipment,status="P")
        return Response(BookingSerializer(customers, many=True).data, status=200)
