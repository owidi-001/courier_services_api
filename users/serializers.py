from rest_framework import serializers
from users.models import User


# USERS and AUTH
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone_number", "email", "avatar", "is_driver"]


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


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """

    email = serializers.EmailField(required=True)


class NewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    new_password = serializers.CharField()
    short_code = serializers.IntegerField()
