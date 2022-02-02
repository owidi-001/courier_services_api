import random

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

from .forms import UserLoginForm, UserCreationForm
from .token_generator import password_reset_token
from .models import User, PasswordResetToken

from django.template.loader import render_to_string

from rest_framework.authtoken.models import Token

from django.conf import settings
from django.core.mail import send_mail
from threading import Thread

# Documentation schema
from .user_doc_schema import *


class EmailThead(Thread):
    def __init__(self, email_to, message):
        super().__init__()
        self.email_to = email_to
        self.message = message

    def run(self):
        send_mail("subject", self.message, settings.EMAIL_HOST_USER, self.email_to,
                  fail_silently=True, html_message=self.message)


# users
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(APIView):
    """
        The user fills the required parameters namely (email,password,username and phone number).
        The form is checked for validity and user saved if valid otherwise relevant exception is thrown.
    """
    schema = RegistrationSchema()

    def post(self, request):
        form = UserCreationForm(request.data)

        if form.is_valid():
            user = form.save()
            data = UserSerializer(user).data
            # create auth token
            token = Token.objects.get(user=user).key
            data["token"] = token
            email_to = form.cleaned_data.get("email")
            message = render_to_string("registration_email.html", {
                "email": email_to})
            EmailThead([email_to], message).start()

            return Response(data, status=200)
        else:
            return Response(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    """
    The user signs in using the email and password used for registering.
    """
    schema = UserLoginSchema()

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
    """
    A user in session can change a password by filling in the old password and filling in the new.
    """
    schema = UpdatePasswordSchema()

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


@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordView(APIView):
    """
    The user fills in email where reset instructions are sent to their email.
    """
    schema = ResetPasswordSchema()

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
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
            message = f'''Password reset code \n Code:{obj.short_token}'''
            message = render_to_string('password_reset_mail.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            EmailThead([email], message).start()

            return Response(
                {"message": f"please check code sent to {email} to change your password", "token": token, "uid": uid64},
                status=200)
        return Response(serializer.errors, status=400)

    @staticmethod
    def gen_token():
        token = ""
        for _ in range(6):
            token += "1234567890"[random.randint(0, 9)]
        return int(token)


