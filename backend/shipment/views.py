from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ShipmentForm
from .models import Origin, Destination
from .serializers import *

from users.data import SUPPORT_CONTACT
from users.models import Driver, User, PasswordResetToken
from users.views import EmailThead

from .models import Shipment, CustomerShipment, Feedback

# Documentation schema
from .shipment_doc_schema import *


# shipment
@method_decorator(csrf_exempt, name='dispatch')
class ShipmentView(APIView):
    permission_classes = (IsAuthenticated,)  # Protect view to only the authenticated
    """
    Returns all shipments which are active and not completed
    """

    def get(self, request):
        query = Shipment.objects.filter(status="A")
        # origin = request.GET.get("origin") or request.GET.get("q")
        # destination = request.GET.get("destination")
        # if origin:
        #     query = query.filter(cargo__origin__name__contains=origin)
        # if destination:
        #     query = query.filter(
        #         route__destination__name__contains=destination)
        response = ShipmentSerializer(query, many=True).data
        return Response(response)

    def post(self, request):
        """
         The client fills in the shipment data
         """
        form = ShipmentForm(request.data)
        if form.is_valid():
            customer = get_object_or_404(User, user=request.user)
            # create cargo
            cargo = Cargo.objects.get_or_create(owner=customer, size=form.cleaned_data["size"],
                                                nature=form.cleaned_data["nature"])
            cargo.save()
            # Create origin
            origin = Origin.objects.get_or_create(lat_position=form.cleaned_data["origin_lat"],
                                                  long_position=form.cleaned_data["origin_long"])
            origin.save()
            # create destination
            destination = Destination.objects.get_or_create(lat_position=form.cleaned_data["dest_lat"],
                                                            long_position=form.cleaned_data["dest_long"])
            destination.save()

            # Book the shipment
            shipment = Shipment.objects.get_or_create(cargo=cargo, origin=origin, destination=destination,
                                                      vehicle=form.cleaned_data["vehicle"])
            shipment.save()

            booking, _ = CustomerShipment.objects.get_or_create(customer=request.user, shipment=shipment, )
            booking.status = "P"
            booking.save()
            message = f"{customer} has booked a shipment from {shipment.origin} to {shipment.destination} \nShipment pending approval"
            EmailThead(["admin@gmail.com"], message)

            data = CustomerShipmentSerializer(booking).data
            return Response(data, status=200)
        return Response(form.errors, status=400)

    def put(self, request):
        """
        Cancel a  booking
        """
        shipment_id = request.data.get("shipment_id")
        customer_booking = get_object_or_404(CustomerShipment, id=shipment_id)
        customer_booking.status = "C"
        customer_booking.save()

        return Response(CustomerShipmentSerializer(customer_booking).data)


@method_decorator(csrf_exempt, name='dispatch')
class DriverShipmentView(APIView):
    """
    Driver get shipment requests
    """
    schema = DriverShipmentSchema()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Returns all driver active shipments
        """
        driver = get_object_or_404(Driver, user=request.user)
        shipments = CustomerShipment.objects.filter(
            shipment.vehicle.driver == driver)  # Filter shipments belonging to the driver
        return Response(CustomerShipmentSerializer(shipments, many=True).data, status=200)

    def put(self, request):
        """
        Driver approves shipment requests
        """
        shipment_id = request.data.get("shipment_id")
        customer_booking = get_object_or_404(CustomerShipment, id=shipment_id)
        customer_booking.confirmed = True
        customer_booking.shipment.status = "A"
        customer_booking.save()

        return Response(CustomerShipmentSerializer(customer_booking).data)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    schema = FeedbackSchema()

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message")
        if message:
            feedback = Feedback(user=request.user,
                                message=message)
            feedback.save()
        return Response({"message": "Thank you for your feed back"}, status=201)


@api_view(["GET"])
def customer_support(request):
    return Response({"phone_numbers": SUPPORT_CONTACT})
