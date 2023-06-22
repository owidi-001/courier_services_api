from rest_framework.permissions import BasePermission
from .models import Driver


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        try:
            driver = Driver.objects.get(user=request.user)
            request.driver = driver
            return True
        except:
            return False
