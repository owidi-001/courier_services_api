from rest_framework import serializers

from .models import Client
from users.serializers import UserSerializer


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ["user", "gender", "is_active"]
