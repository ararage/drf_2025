from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

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

        self.movie_title = "Example Movie"
        self.watchlist = models.WatchList.objects.create(
            title=self.movie_title,
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

    def test_watchlist_list(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse("movie-detail", args=(self.watchlist.uuid,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, self.movie_title)
        self.assertEqual(models.WatchList.objects.count(), 1)


class ReviewTestCase(APITestCase):

    def setUp(self):
        user_data = {
            "username": "example",
            "password": "example123",
            "is_staff": False,
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
        self.watchlist_2 = models.WatchList.objects.create(
            title="Example Movie 2",
            storyline="An example movie storyline 2.",
            platform=self.stream,
            active=True,
        )
        self.review = models.Reviews.objects.create(
            review_user=self.user,
            rating=5,
            description="Great movie!",
            watchlist=self.watchlist_2,
            active=True,
        )

    def test_review_create(self):
        data = {
            "rating": 4,
            "description": "Great movie!",
            # "watchlist": str(self.watchlist_2.uuid),
        }
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.uuid,)), data
        )
        created_uuid = response.data.get("uuid")
        review_obj = models.Reviews.objects.get(uuid=created_uuid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Reviews.objects.count(), 2)
        self.assertEqual(str(review_obj.watchlist.uuid), str(self.watchlist.uuid))
        self.assertEqual(review_obj.rating, data["rating"])
        self.assertEqual(review_obj.description, data["description"])

        # Duplicate Validation
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.uuid,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_as_anonymous(self):
        self.client.force_authenticate(user=None)  # Logout
        data = {
            "rating": 5,
            "description": "Amazing movie!",
            "watchlist": str(self.watchlist.uuid),
        }
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.uuid,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_update(self):
        data = {
            "rating": 4,
            "description": "[Update] Good movie",
            "watchlist": str(self.watchlist_2.uuid),
        }
        response = self.client.put(
            reverse("review-detail", args=(self.review.uuid,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Reviews.objects.count(), 1)
        self.assertEqual(models.Reviews.objects.get().rating, 4)
        self.assertEqual(
            models.Reviews.objects.get().description, "[Update] Good movie"
        )

    def test_review_list(self):
        response = self.client.get(reverse("review-list", args=(self.watchlist.uuid,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Reviews.objects.count(), 1)

    def test_delete_review(self):
        response = self.client.delete(
            reverse("review-detail", args=(self.review.uuid,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Reviews.objects.count(), 0)

    def test_review_user(self):
        response = self.client.get(f"/watch/reviews/?username={self.user.username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
