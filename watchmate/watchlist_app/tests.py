from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        user_data = {
            "username": "example",
            "password": "example123",
            "is_staff": True,
        }
        self.user = User.objects.create_user(**user_data)
        response = self.client.post(reverse("token_obtain_pair"), user_data)
        self.access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

        self.stream = models.StreamPlatform.objects.create(
            name="Hulu",
            about="Streaming Platform",
            website="https://www.hulu.com",
        )

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Streaming Platform",
            "website": "https://www.netflix.com",
        }
        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(
            reverse("streamplatform-detail", args=(self.stream.uuid,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_update(self):
        data = {
            "name": "Hulu Updated",
            "about": "Streaming Platform Updated",
            "website": "https://www.hulu.com/updated",
        }
        response = self.client.put(
            reverse("streamplatform-detail", args=(self.stream.uuid,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_delete(self):
        response = self.client.delete(
            reverse("streamplatform-detail", args=(self.stream.uuid,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WatchListTestCase(APITestCase):

    def setUp(self):
        user_data = {
            "username": "example",
            "password": "example123",
            "is_staff": True,
        }
        self.user = User.objects.create_user(**user_data)
        response = self.client.post(reverse("token_obtain_pair"), user_data)
        self.access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

        self.stream = models.StreamPlatform.objects.create(
            name="Hulu",
            about="Streaming Platform",
            website="https://www.hulu.com",
        )

        self.watchlist = models.WatchList.objects.create(
            title="Example Movie",
            storyline="An example movie storyline.",
            platform=self.stream,
            active=True,
        )

    def test_watchlist_create(self):
        data = {
            "title": "New Movie",
            "storyline": "A new movie storyline.",
            "platform": str(self.stream.uuid),
        }
        response = self.client.post(reverse("movie-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
