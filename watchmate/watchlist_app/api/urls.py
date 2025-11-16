from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (
    WatchListDetailAPIView,
    StreamPlatformAPIView,
    StreamPlatformDetailAPIView,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformViewSet,
    StreamPlatformModelViewSet,
    ReviewUserList,
    ReviewsByUserList,
    WatchListAPIView,
    WatchListGenericListV2APIView,
    WatchListGenericListV3APIView,
    WatchListGenericListV4APIView,
)

router = DefaultRouter()
router.register("stream", StreamPlatformViewSet, basename="streamplatform")

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_detail, name='movie-detail'),
    path("v1/list/", WatchListAPIView.as_view(), name="movie-list"),
    path("v2/list/", WatchListGenericListV2APIView.as_view(), name="movie-list-2"),
    path("v3/list/", WatchListGenericListV3APIView.as_view(), name="movie-list-3"),
    path("v4/list/", WatchListGenericListV4APIView.as_view(), name="movie-list-4"),
    re_path(
        r"(?P<pk>[0-9a-f-]+)/$",
        WatchListDetailAPIView.as_view(),
        name="movie-detail",
    ),
    path("", include(router.urls)),
    # path("stream/", StreamPlatformAPIView.as_view(), name="streamplatform-list"),
    # re_path( r"stream/(?P<pk>[0-9a-f-]+)/$", StreamPlatformDetailAPIView.as_view(), name="streamplatform-detail"),
    # path("review/", ReviewList.as_view(), name="review-list"),
    # re_path(r"review/(?P<pk>[0-9a-f-]+)/$",ReviewDetail.as_view(),name="review-detail"),
    re_path(
        r"(?P<pk>[0-9a-f-]+)/review-create",
        ReviewCreate.as_view(),
        name="review-create",
    ),
    re_path(r"(?P<pk>[0-9a-f-]+)/reviews", ReviewList.as_view(), name="review-list"),
    # re_path(r"watchlist/(?P<pk>[0-9a-f-]+)/review", ReviewList.as_view(), name="review-create"),
    re_path(
        r"review/(?P<pk>[0-9a-f-]+)/$",
        ReviewDetail.as_view(),
        name="review-detail",
    ),
    path("my_reviews/", ReviewUserList.as_view(), name="user-review-list"),
    path("reviews/", ReviewsByUserList.as_view(), name="user-review-list"),
]
