from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shipment.models import CustomerShipment
# Documentation schema
from .client_doc_schema import *
from .forms import ClientProfileUpdateForm
from .models import User
from .serializers import *


# Customer
@method_decorator(csrf_exempt, name='dispatch')
class ClientProfileView(APIView):
    """
        Returns the basic saved customer details such as email,username, phone and shipments.
    """
    schema = ClientSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def client_active(self, request):
        """
        Activate client when he or she has made at least one shipment
        """
        client = get_object_or_404(Client, user=request.user)
        shipments = CustomerShipment.objects.filter(customer=client)

        if len(shipments) > 0 and not client.is_active:
            client.is_active = True
            client.save()

        return client

    def get(self, request):
        """
        Returns user profile
        """
        client = self.client_active(request)

        response = ClientSerializer(client).data
        return Response(response, status=200)

    def put(self, request):
        """update profile - email, phone number,avatar"""
        form = ClientProfileUpdateForm(request.data)
        if form.is_valid():

            client = get_object_or_404(Client, user=request.user)

            if form.cleaned_data.get("email"):
                client.user.email = form.cleaned_data["email"]
                client.user.save()
            if form.cleaned_data.get("phone_number"):
                client.user.phone_number = form.cleaned_data['phone_number']
                client.user.save()
            if form.cleaned_data.get("gender"):
                client.gender = form.cleaned_data['gender']
                client.save()
            client.save()
            return Response(ClientSerializer(client).data, status=status.HTTP_200_OK)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """update client avatar"""
        if request.FILES:
            profile = User.objects.get(
                user=request.user
            )
            profile.avatar = request.FILES[0]
            profile.save()
            return Response({"message": "avatar updated successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "invalid image"}, status=status.HTTP_400_BAD_REQUEST)
