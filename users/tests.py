from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='notme', email='notme@gmail.com', phone_number="+254709678543")
        User.objects.create(username='notme1', email='notme1@gmail.com', phone_number="+254709578543", is_driver=True)

    def test_username_label(self):
        client = User.objects.get(id=1)
        field_label = client._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_driver_creation(self):
        user = User.objects.get(id=1)
        user1 = User.objects.get(id=2)
        self.assertEqual(user.is_driver, False)
        self.assertEqual(user1.is_driver, True)

    def test_str(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.__str__(), user.email)

    # def test_get_absolute_url(self):
    #     user = User.objects.get(id=1)
    #     self.assertEqual(user.get_absolute_url(), 'user/1')
