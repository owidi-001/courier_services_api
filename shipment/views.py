from django.db.models.fields import json
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import *

from users.data import SUPPORT_CONTACT
from users.models import Driver, User, PasswordResetToken
from users.views import EmailThead

from .models import Location, Shipment, CustomerShipment, Feedback

# Documentation schema
from .shipment_doc_schema import *


# shipment
@method_decorator(csrf_exempt, name="dispatch")
class ShipmentView(APIView):
    schema = ShipmentSchema()
    # Protect view to only the authenticated
    permission_classes = (IsAuthenticated,)

    """
    Returns all user shipments 
    """

    def get(self, request):
        query = CustomerShipment.objects.filter(customer=request.user)
        response = CustomerShipmentSerializer(query, many=True).data
        return Response(response)

    """
    Saves all shipment information filled by the customer.
    """

    def post(self, request):
        """
        The client fills in the shipment data
        """
        shimpment_serializer = ShipmentSerializer(data=request.data)
        if shimpment_serializer.is_valid():
            shipment = shimpment_serializer.save(
                request,
            )
            data = CustomerShipmentSerializer(
                shipment,
            ).data
            return Response(data, status=200)
        return Response(shimpment_serializer.errors, status=400)

    def patch(self, request):
        """
        Cancel a  shipment
        """
        shipment_id = request.data.get("shipment_id")
        customer_shipment = get_object_or_404(CustomerShipment, id=shipment_id)
        customer_shipment.shipment.status = "C"
        customer_shipment.shipment.save()
        # Mail customer to affirm shipment cancellation
        message = f"You have successfully cancelled the shipment request"
        EmailThead(
            [customer_shipment.customer.email, "courier_admin@gmail.com"], message
        )
        return Response(CustomerShipmentSerializer(customer_shipment).data)


@method_decorator(csrf_exempt, name="dispatch")
class VehicleView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    Returns all vehicle available
    """

    def get(self, request):
        """
        Returns all vehicle available
        """
        query = Vehicle.objects.all()

        return Response(
            VehicleSerializer(query, many=True).data,
            status=200,
        )


@method_decorator(csrf_exempt, name="dispatch")
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
        query = Shipment.objects.filter(status="A")
        driver = get_object_or_404(Driver, user=request.user)
        shipments = []
        [
            shipments.append(shipment)
            for shipment in query
            if shipment.vehicle.driver == driver
        ]
        # shipments= CustomerShipment.objects.filter(driver=driver)  # Filter shipments belonging to the driver

        return Response(
            CustomerShipmentSerializer(shipments, many=True).data, status=200
        )

    def put(self, request):
        """
        Driver approves shipment requests
        """
        shipment_id = request.data.get("shipment_id")
        customer_shipment = get_object_or_404(CustomerShipment, id=shipment_id)
        customer_shipment.confirmed = True
        customer_shipment.shipment.status = "A"
        customer_shipment.save()
        # Mail customer to affirm shipment in progress.
        message = f"{request.user} has confirmed your shipment set fom {customer_shipment.shipment.origin} to {customer_shipment.shipment.destination}"
        EmailThead(
            [customer_shipment.customer.email, "courier_admin@gmail.com"], message
        )
        return Response(CustomerShipmentSerializer(customer_shipment).data)

    def patch(self, request):
        """
        Driver affirms shipment completion
        """
        shipment_id = request.data.get("shipment_id")
        customer_shipment = get_object_or_404(CustomerShipment, id=shipment_id)
        if customer_shipment.status == "A":
            customer_shipment.shipment.status = "F"
        customer_shipment.save()
        # Mail customer to affirm shipment is completed.
        message = (
            f"Your shipment if complete.\nWe value your feedback. Please leave us a review. Thank you for "
            f"trusting us. "
        )
        EmailThead(
            [customer_shipment.customer.email, "courier_admin@gmail.com"], message
        )
        return Response(CustomerShipmentSerializer(customer_shipment).data)


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackView(APIView):
    schema = FeedbackSchema()

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Provide overal feed back on our services"""
        message = request.data.get("message")
        if message:
            feedback = Feedback(user=request.user, message=message)
            feedback.save()
        return Response({"message": "Thank you for your feed back"}, status=201)

    def put(self, request):
        """Rate a shipment delivery"""
        try:
            rating = float(request.data.get("rating"))
            shipmentId = int(request.data.get("shipment_id"))
            shipment = Shipment.objects.get(id=shipmentId)
            shipment.rating = rating
            shipment.save()
        except:
            return Response("An error occured")
        return Response({"message": "Thank you for your feed back"})


@api_view(["GET"])
def customer_support(request):
    return Response({"phone_numbers": SUPPORT_CONTACT})
