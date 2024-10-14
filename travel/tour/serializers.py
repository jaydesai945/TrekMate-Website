# tours/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organizer, Place, Hotel, Trip, Booking, Review, PlaceImage
from django.contrib.auth import authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'liked_trips')
        read_only_fields = ('liked_trips',)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, read_only=True)
    hotel = HotelSerializer(many=True, read_only=True)
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Review
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    is_past_trip = serializers.SerializerMethodField()
    is_current_trip = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'trip',
            'booking_date',
            'num_people',
            'total_cost',
            'is_past_trip',
            'is_current_trip'
        ]

    def get_is_past_trip(self, obj):
        return obj.is_past_trip()

    def get_is_current_trip(self, obj):
        return obj.is_current_trip()

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'image', 'caption']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        return {
            'user': user
        }