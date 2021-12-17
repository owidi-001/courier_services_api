from abc import ABC

from rest_framework import serializers
from users.models import User, Customer, Driver


# USERS and AUTH
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["national_id", "phone_number", "email"]


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ["id", "user", "national_id", "phone_number", "email"]


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ["id", "user", "phone_number", "dl_number", "national_id_number", "gender"]


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
