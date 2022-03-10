from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from driver.permision import IsDriver


from .serializers import *

from users.data import SUPPORT_CONTACT
from users.views import EmailThead

from .models import Notification, Shipment, CustomerShipment, Feedback

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
            message = "You shipment request has been received."
            notification = Notification(
                user=request.user,
                message=message
            )
            notification.save()
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
        notification = Notification(
            user=request.user,
            message=message
        )
        notification.save()
        return Response(CustomerShipmentSerializer(customer_shipment).data)


class DriverShipmentsView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def get(self, request):
        """
        Returns all driver shipments - shipment history
        """
        query = CustomerShipment.objects.filter(
            shipment__vehicle__driver=request.driver)

        return Response(
            CustomerShipmentSerializer(query, many=True).data,
        )


@method_decorator(csrf_exempt, name="dispatch")
class DriverShipmentRequestView(APIView):
    """
    Driver get shipment requests
    """

    schema = DriverShipmentSchema()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsDriver]

    def get(self, request, **kwargs):
        """
        Returns all shipment requests for a driver  driver 
        """
        query = CustomerShipment.objects.filter(
            shipment__status="P")
        query = query.filter(shipment__vehicle__driver=request.driver)

        return Response(
            CustomerShipmentSerializer(query, many=True).data,
        )

    def put(self, request):
        """
        Driver approves customer shipment requests
        """
        shipment_id = request.data.get("shipment_id")
        customer_shipment = get_object_or_404(CustomerShipment, id=shipment_id)

        customer_shipment.confirmed = True
        customer_shipment.shipment.status = "A"

        customer_shipment.save()
        customer_shipment.shipment.save()
        try:
            message = f"{request.user} has confirmed your shipment set fom {customer_shipment.shipment.origin} to {customer_shipment.shipment.destination}"
            EmailThead(
                [customer_shipment.customer.email,
                    "courier_admin@gmail.com"], message
            )

            notification = Notification(
                user=customer_shipment.customer,
                message=message
            )
            notification.save()
        except:
            pass

        return Response(CustomerShipmentSerializer(customer_shipment).data)

    def patch(self, request):
        """
        Driver affirms customer shipment completion
        """

        shipment_id = request.data.get("shipment_id")
        customer_shipment = get_object_or_404(CustomerShipment, id=shipment_id)
        if customer_shipment.shipment.status == "A":
            customer_shipment.shipment.status = "F"
        customer_shipment.shipment.save()
        try:
            # Mail customer to affirm shipment is completed.
            message = (
                f"Your shipment if complete.\nWe value your feedback. Please leave us a review. Thank you for "
                f"trusting us. "
            )
            EmailThead(
                [
                    customer_shipment.customer.email,
                    "courier_admin@gmail.com",
                ],
                message,
            )
            notification = Notification(
                user=customer_shipment.customer,
                message=message
            )
            notification.save()
        except:
            pass
        return Response(
            CustomerShipmentSerializer(customer_shipment).data,
        )


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackView(APIView):
    schema = FeedbackSchema()

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Rate a shipment delivery"""
        rating = request.data.get("rating")
        shipmentId = request.data.get("shipment_id")
        shipment = get_object_or_404(Shipment, id=shipmentId)
        if rating:
            shipment.rating = rating
        shipment.save()
        message = request.data.get("message")
        if message:
            feedback = Feedback(user=request.user,
                                message=message, shipment=shipment)
            feedback.save()

        return Response({"message": "Thank you for your feed back"})


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        data = NotificationSerializer(notifications, many=True).data
        return Response(data)


@api_view(["GET"])
def customer_support(request):
    return Response({"phone_numbers": SUPPORT_CONTACT})
