from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (
    WatchListAPIView,
    WatchListDetailAPIView,
    StreamPlatformAPIView,
    StreamPlatformDetailAPIView,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformViewSet,
    StreamPlatformModelViewSet
)

router = DefaultRouter()
router.register(
    'stream',
    StreamPlatformViewSet,
    basename='streamplatform'
)

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_detail, name='movie-detail'),
    path("list/", WatchListAPIView.as_view(), name="movie-list"),
    re_path(
        r"(?P<pk>[0-9a-f-]+)/$",
        WatchListDetailAPIView.as_view(),
        name="movie-detail",
    ),
    path('', include(router.urls)),
    
    # path("stream/", StreamPlatformAPIView.as_view(), name="streamplatform-list"),
    # re_path( r"stream/(?P<pk>[0-9a-f-]+)/$", StreamPlatformDetailAPIView.as_view(), name="streamplatform-detail"),
    
    
    # path("review/", ReviewList.as_view(), name="review-list"),
    # re_path(r"review/(?P<pk>[0-9a-f-]+)/$",ReviewDetail.as_view(),name="review-detail"),
    re_path(
        r"(?P<pk>[0-9a-f-]+)/review-create", ReviewCreate.as_view(), name="review-create"
    ),
    re_path(
        r"(?P<pk>[0-9a-f-]+)/reviews", ReviewList.as_view(), name="review-list"
    ),
    # re_path(r"watchlist/(?P<pk>[0-9a-f-]+)/review", ReviewList.as_view(), name="review-create"),
    re_path(
        r"review/(?P<pk>[0-9a-f-]+)/$",
        ReviewDetail.as_view(),
        name="review-detail",
    ),
]
