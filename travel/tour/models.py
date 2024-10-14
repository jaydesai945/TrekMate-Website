# tours/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta, date

class User(AbstractUser):
    liked_trips = models.ManyToManyField('Trip', related_name='liked_by', blank=True)

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    image = models.ImageField(upload_to='places/')
    famous_food = models.TextField()
    featured = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    celebrated_festivals = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotels/')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Trip(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    organizer = models.ForeignKey(Organizer, related_name='trips', on_delete=models.CASCADE)
    places = models.ManyToManyField(Place, related_name='trips')
    hotel = models.ManyToManyField(Hotel, related_name='trips')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text='Duration in days')
    transportation_medium = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} by {self.organizer.name}"


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, related_name='reviews', on_delete=models.CASCADE,default=1)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.trip}"

class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, related_name='bookings', on_delete=models.CASCADE)
    booking_date = models.DateField()
    num_people = models.PositiveIntegerField(default=1)  # Number of people for the booking
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total cost of the booking

    def __str__(self):
        return f"Booking by {self.user.username} for {self.trip} with {self.num_people} people"

    def is_past_trip(self):
        end_date = self.booking_date + timedelta(days=self.trip.duration)
        return end_date < date.today()

    def is_current_trip(self):
        end_date = self.booking_date + timedelta(days=self.trip.duration)
        return self.booking_date <= date.today() <= end_date

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='place_images/')
    caption = models.CharField(max_length=255, blank=True)  # Optional caption for each image

    def __str__(self):
        return f"Image for {self.place.name} - {self.caption}"
    
