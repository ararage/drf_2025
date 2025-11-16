from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins, viewsets, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    ScopedRateThrottle,
)

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

from watchlist_app.api.pagination import (
    WatchListPagination,
    WatchListLimitOffsetPagination,
    WatchListCursorPagination,
)


class ReviewsByUserList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Reviews.objects.filter()
        # username = self.kwargs['username']
        username = self.request.query_params.get("username", None)
        if username:
            queryset = queryset.filter(review_user__username=username)
        return queryset


class ReviewUserList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    def get_queryset(self):
        return Reviews.objects.filter(review_user=self.request.user)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        queryset = WatchList.objects.filter(active=True)
        watchlist = get_object_or_404(queryset, pk=pk)

        review_user = self.request.user if self.request.user.id else None

        review_queryset = Reviews.objects.filter(
            watchlist=watchlist, review_user__isnull=False
        )

        if review_user:
            review_queryset = review_queryset.filter(
                review_user=review_user.id,
            )

        if review_user and review_queryset.exists():
            raise ValidationError("You have already reviewd this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data["rating"]
            ) / 2

        watchlist.number_rating = watchlist.number_rating + 1

        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Reviews.objects.filter(watchlist=pk)


"""
class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user if self.request.user.id else None
        
        review_queryset = Reviews.objects.filter(
            watchlist=watchlist,
            review_user__isnull=False
        )
        
        if review_user:
            review_queryset.filter(
                review_user=review_user.id,
            )
            
        if review_user and review_queryset.exists():
            raise ValidationError("You have already reviewd this movie!")
        
        serializer.save(
            watchlist=watchlist,
            review_user=review_user
        )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Reviews.objects.filter(watchlist=pk)
"""


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "review-detail"


"""
class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ReviewList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""


class StreamPlatformModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StreamPlatform.objects.filter(active=True)
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class StreamPlatformViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlatform.objects.filter(active=True)
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.filter(active=True)
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        platform.active = False
        platform.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            serializer.data,
        )


class StreamPlatformAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platforms, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)


class StreamPlatformDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            serializer.data,
        )

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGenericListV2APIView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["^title", "platform__name"]
    ordering_fields = ["avg_rating"]
    pagination_class = WatchListPagination


class WatchListGenericListV3APIView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["^title", "platform__name"]
    ordering_fields = ["avg_rating"]
    pagination_class = WatchListLimitOffsetPagination


class WatchListGenericListV4APIView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ["^title", "platform__name"]
    # ordering_fields = ["avg_rating"]
    pagination_class = WatchListCursorPagination


class WatchListAPIView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, _):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)


class WatchListDetailAPIView(APIView):

    permissions = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            serializer.data,
        )

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    serializer = MovieSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)    
    serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(
            {'message': 'Movie not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'PUT':
        serializer = MovieSerializer(
            movie,
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            serializer.data,
        )
    if request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Default Case GET
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
"""
