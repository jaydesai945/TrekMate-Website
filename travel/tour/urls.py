from django.urls import path
from .views import (
    RegisterView, LoginView, UserProfileView, SaveLikedTripView,
    OrganizerListView, PlaceListView, HotelListView, TripListView,
    ReviewListCreateView, ReviewListView, BookingListCreateView,
    PastTripListView, CurrentTripListView, PlaceImageListView,
    TripDetailView, PlaceDetailView, ReviewDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('save-liked-trip/', SaveLikedTripView.as_view(), name='save-liked-trip'),
    
    path('organizers/', OrganizerListView.as_view(), name='organizer-list'),
    path('places/', PlaceListView.as_view(), name='place-list'),
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('trips/', TripListView.as_view(), name='trip-list'),
    
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/list/', ReviewListView.as_view(), name='review-list'),
    
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/past/', PastTripListView.as_view(), name='past-trip-list'),
    path('bookings/current/', CurrentTripListView.as_view(), name='current-trip-list'),
    
    path('places/<int:place_id>/images/', PlaceImageListView.as_view(), name='place-image-list'),
    
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('places/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
