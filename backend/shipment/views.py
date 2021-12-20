from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ShipmentForm
from .serializers import *

from users.data import SUPPORT_CONTACT
from users.models import Customer, Driver, User, EmailThead, PasswordResetToken

from shipment.models import Shipment, CustomerShipment, Feedback

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
        origin = request.GET.get("from") or request.GET.get("q")
        destination = request.GET.get("to")
        if origin:
            query = query.filter(cargo__origin__name__contains=origin)
        if destination:
            query = query.filter(
                route__destination__name__contains=destination)
        response = ShipmentSerializer(query, many=True).data
        return Response(response)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerShipmentView(APIView):
    """
    customer car booking view
    """
    schema = CustomerShipmentSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns all customer bookings
        """
        customer = get_object_or_404(Customer, user=request.user)
        bookings = CustomerShipment.objects.filter(customer=customer)
        return Response(CustomerShipmentSerializer(bookings, many=True).data, status=200)

    def post(self, request):
        """
         customer to book the cargo shipment
         """
        form = ShipmentForm(request.data)
        if form.is_valid():
            shipment = get_object_or_404(Shipment, id=form.cleaned_data["shipment_id"])

            customer = get_object_or_404(Customer, user=request.user)
            booking, _ = CustomerShipment.objects.get_or_create(customer=customer, shipment=shipment, )

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Returns all driver active shipments
        """
        driver = get_object_or_404(Driver, user=request.user)
        shipments = CustomerShipment.objects.filter(
            driver=driver)  # Filter shipments belonging to the driver
        return Response(CustomerShipmentSerializer(shipments, many=True).data, status=200)

    def put(self, request):
        """
        Driver approves shipment requests
        """
        shipment_id = request.data.get("shipment_id")
        customer_booking = get_object_or_404(CustomerShipment, id=shipment_id)
        customer_booking.confirmed = True
        customer_booking.status = "A"
        customer_booking.save()

        return Response(CustomerShipmentSerializer(customer_booking).data)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):

    schema = FeedbackSchema()

    authentication_classes = [TokenAuthentication]
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
