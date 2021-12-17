from abc import ABC

from rest_framework import serializers
from users.models import User, Customer, Driver


# USERS and AUTH
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["national_id", "phone_number", "email"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "national_id", "phone_number", "email"]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "phone_number", "dl_number", "national_id_number", "gender"]


# API serializer classes
# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = ["email", "password"]


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint .
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """
    email = serializers.EmailField(required=True)


class NewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    new_password = serializers.CharField()
    short_code = serializers.IntegerField()
