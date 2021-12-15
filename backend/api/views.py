import random
from threading import Thread

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

from users.data import SUPPORT_CONTACT
from users.forms import UserLoginForm, UserProfileUpdateForm, UserCreationForm, AddressUpdateForm
from users.token_generator import password_reset_token
from users.models import Customer, UserAddress, City, Street, Address, User, PasswordResetToken

from shipment.models import Shipment, CustomerBooking, Feedback

'''
contains documentation schema
'''
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.authtoken.models import Token


# create a thread to send email
class EmailThead(Thread):
    def __init__(self, email_to, message):
        super().__init__()
        self.email_to = email_to
        self.message = message

    def run(self):
        send_mail("subject", self.message, settings.EMAIL_HOST_USER, self.email_to,
                  fail_silently=True, html_message=self.message)


# Customer registration
@method_decorator(csrf_exempt, name='dispatch')
class RegisterCustomer(APIView):

    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            data = UserSerializer(user).data
            # create auth token
            token = Token.objects.get(user=user).key
            data["token"] = token
            email_to = form.cleaned_data.get("email")
            password = form.cleaned_data["password"]
            message = render_to_string("registration_email.html", {
                "password": password, "email": email_to})
            EmailThead([email_to], message).start()

            return Response(data, status=200)
        else:
            return Response(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    """
    login user
    """

    def post(self, request):
        form = UserLoginForm(request.data)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"],
                                password=form.cleaned_data["password"])
            if user:
                token = Token.objects.get(user=user).key
                data = UserSerializer(user).data
                data["token"] = token
                return Response(data, status=200)
            return Response({"errors": ["please provide valid credentials"]},
                            status=400)
        return Response(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=200)
        return Response(serializer.errors, status=400)


def put(request):
    serializer = NewPasswordSerializer(data=request.data)
    if serializer.is_valid():

        uidb64 = request.data.get("uid")
        try:
            short_code = int(request.data.get('short_code'))
            uid = int(force_bytes(urlsafe_base64_decode(uidb64)))
            password_token = PasswordResetToken.objects.get(
                user=uid, short_token=short_code)
        except(TypeError, ValueError, OverflowError, PasswordResetToken.DoesNotExist):
            return Response({"message": "The cofirmation code is invalid or it has expired"}, status=400)

        if password_reset_token.check_token(password_token.user, password_token.reset_token):
            user = get_object_or_404(User, id=uid)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            password_token.delete()
            return Response({"message": "Your password has been changed successfuly "}, status=201)
        else:
            return Response({"message": "Your token has expired please generate another token "}, status=400)
    return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            user = User.objects.filter(
                email=email).first()
            if not user:
                return Response({"email": ["User not found"]}, status=400)
            site = get_current_site(request)
            '''
            short code to be used to change password
            short code will be sent to the user which will be used to reset the password 
            instead of sending long password reset token generated by django PasswordResetGenerator 
            '''
            token = password_reset_token.make_token(user)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            try:
                PasswordResetToken.objects.get(user=user).delete()
            except:
                pass
            obj = PasswordResetToken(user=user,
                                     short_token=self.gen_token(),
                                     reset_token=token)
            obj.save()
            # send short_token to user email
            # message = f'''Password reset code \n Code:{obj.short_token}'''
            message = render_to_string('password_reset_mail.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            EmailThead([email], message).start()

            return Response({"message": f"please check code sent to {email} to change your password","token":token, "uid": uid64},
                            status=200)
        return Response(serializer.errors, status=400)

    @staticmethod
    def gen_token():
        token = ""
        for _ in range(6):
            token += "1234567890"[random.randint(0, 9)]
        return int(token)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerProfileView(APIView):
    """
    customer view
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns customer profile
        """

        customer_profile = get_object_or_404(Customer, user=request.user)
        response = CustomerProfileSerializer(customer_profile).data
        return Response(data=response, status=200)

    def put(self, request):
        """update profile - email, phone number"""
        form = UserProfileUpdateForm(request.data)
        if form.is_valid():
            user = request.user
            customer_profile = get_object_or_404(Customer, user=user)
            if form.cleaned_data.get("email"):
                user.email = form.cleaned_data["email"]
                user.save()
            if form.cleaned_data.get("phone_number"):
                customer_profile.phone_number = form.cleaned_data['phone_number']
            customer_profile.save()
            return Response(CustomerProfileSerializer(customer_profile).data,
                            status=200)

        return Response(form.errors, status=400)

    def patch(self, request):
        """update customer profile image"""
        if request.FILES:
            profile = Customer.objects.get(
                user=request.user
            )
            profile.profile_image = request.FILES[0]
            profile.save()
            return Response({"message": "profile update was successful"}, status=200)
        return Response({"message": "invalid image"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ShipmentView(APIView):
    """
    Returns all shipment which are active and not completed
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
class CustomerBookingView(APIView):
    """
    customer car booking view
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns all customer bookings
        """
        customer = get_object_or_404(Customer, user=request.user)
        bookings = CustomerBooking.objects.filter(customer=customer)
        return Response(BookingSerializer(bookings, many=True).data, status=200)

    # def post(self, request):
    #     """
    #      customer to book the cargo shipment
    #      """
    #     form = BookingForm(request.data)
    #     if form.is_valid():
    #         num_seats = form.cleaned_data["seats_number"]
    #
    #         trip = get_object_or_404(Trip, id=form.cleaned_data["trip_id"])
    #
    #         customer = get_object_or_404(
    #             Customer, user=request.user)
    #         booking, _ = CustomerBooking.objects.get_or_create(
    #             customer=customer,
    #             trip=trip,
    #
    #         )
    #         booking.seats = num_seats
    #         booking.status = "A"
    #         booking.save()
    #         message = f'''{request.user} has booked a trip from
    #                      {trip.route.origin} to {trip.route.destination}'''
    #         EmailThead(["xxxyyyzzz@gmail.com"], message)

    #         data = BookingSerializer(booking).data
    #         return Response(data, status=200)
    #     return Response(form.errors, status=400)

    def put(self, request):
        """
        Cancel a  booking
        """
        book_id = request.data.get("book_id")
        customer_booking = get_object_or_404(CustomerBooking, id=book_id)
        customer_booking.status = "C"
        customer_booking.save()

        return Response(BookingSerializer(customer_booking).data)


@method_decorator(csrf_exempt, name='dispatch')
class UserAddressView(APIView):
    """
     user address view
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a  list of user addresses
        """
        address = UserAddress.objects.filter(user=request.user)
        return Response(UserAddressSerializer(address, many=True).data)

    def post(self, request, *args, **kwargs):
        """'
        create user address
        """
        form = AddressUpdateForm(request.data)
        user = request.user
        if form.is_valid():
            city = City.objects.filter(
                name__iexact=form.cleaned_data["city"]).first()
            if not city:
                city = City.objects.create(
                    name=form.cleaned_data["city"])
            street = Street.objects.filter(
                name__iexact=form.cleaned_data["street"]).first()
            if not street:
                street = Street.objects.create(
                    name=form.cleaned_data["street"])
            address, created = Address.objects.get_or_create(street=street, city=city,
                                                             zip_code=form.cleaned_data["zip_code"])
            if created:
                address.save()
                user_address, _ = UserAddress.objects.get_or_create(
                    user=user,
                    address=address
                )
                user_address.save()
            return Response(AddressSerializer(address).data)
        return Response(form.errors, status=400)

    def delete(self, request, *args, **kwargs):
        address = get_object_or_404(Address, id=request.data.get("address_id"))
        address.delete()
        return Response(AddressSerializer(address).data)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
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
