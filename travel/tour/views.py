from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Organizer, Place, Hotel, Trip, Booking, Review, PlaceImage
from .serializers import (
    UserSerializer, RegisterSerializer, OrganizerSerializer, PlaceSerializer,
    HotelSerializer, TripSerializer, BookingSerializer, ReviewSerializer, PlaceImageSerializer, LoginSerializer
)
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import TripFilter
from django.utils.timezone import now

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': RegisterSerializer(user).data["username"],
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': str(user),
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class SaveLikedTripView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        trip_id = request.data.get('trip_id')
        action = request.data.get('action')
        try:
            trip = Trip.objects.get(id=trip_id)
            if action == 'save':
                request.user.liked_trips.add(trip)
            elif action == 'unsave':
                request.user.liked_trips.remove(trip)
            return Response({'status': 'Trip saved/unsaved successfully'})
        except Trip.DoesNotExist:
            return Response({'error': 'Trip does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class OrganizerListView(generics.ListAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [permissions.AllowAny]

class PlaceListView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state', 'celebrated_festivals', 'description']

class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]

class TripListView(generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TripFilter
    ordering_fields = '__all__'
    ordering = ['id']

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Review.objects.all()
        user_id = self.request.query_params.get('user', None)
        trip_id = self.request.query_params.get('trip', None)

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)

        return queryset

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        trip = serializer.validated_data['trip']
        num_people = serializer.validated_data['num_people']
        total_cost = trip.price * num_people  # Calculate total cost based on trip price and number of people
        serializer.save(user=self.request.user, total_cost=total_cost)

class PastTripListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = now().date()
        queryset = Booking.objects.filter(user=self.request.user)
        # Compute the end date of the trip manually
        past_trips = []
        for booking in queryset:
            end_date = booking.booking_date + timedelta(days=booking.trip.duration)
            if end_date < today:
                past_trips.append(booking.id)
        return queryset.filter(id__in=past_trips)

class CurrentTripListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
 

    def get_queryset(self):
        today = now().date()
        queryset = Booking.objects.filter(user=self.request.user)
        # Filter trips that start today or in the future
        upcoming_trips = []
        for booking in queryset:
            end_date = booking.booking_date + timedelta(days=booking.trip.duration)
            # Include trips where the end date is in the future (upcoming trips)
            if end_date >= today:  # Trip is either ongoing or upcoming
                upcoming_trips.append(booking.id)
        return queryset.filter(id__in=upcoming_trips)


class PlaceImageListView(generics.ListAPIView):
    serializer_class = PlaceImageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        return PlaceImage.objects.filter(place_id=place_id)

class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.AllowAny]

class PlaceDetailView(generics.RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Optionally, you can include additional logic here if needed
        serializer.save()