from django.conf import settings
from django.test import TestCase
from .models import User


# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create("marangisir@protonmail.com", "sir", "marangi")
        User.objects.create("mrmarangi4@gmail.com", "Mr", "marangi")

    def test_create_user(self):
        user1 = User.objects.get(email="marangisir@protonmail.com")
        user2 = User.objects.get(email="mrmarangi4@gmail.com")

        self.AssertEqual(user1.__str__(), "marangisir@protonmail.com")
        self.AssertEqual(user2.__str__(), "mrmarangi4@gmail.com")
