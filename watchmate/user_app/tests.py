from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def test_register_user(self):
        data = {
            "username": "testcase",
            "password": "testcase123",
            "password2": "testcase123",
            "email": "testcase@test.com",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase", password="testcase123"
        )

    def test_login_user(self):
        data = {"username": "testcase", "password": "testcase123"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    """
