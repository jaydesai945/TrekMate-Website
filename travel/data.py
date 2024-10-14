from tour.models import User, Organizer, Place, Hotel, Trip, Review, Booking, PlaceImage
from datetime import date
import random

# Utility function to create random dates
def random_date(year):
    return date(year, random.randint(1, 12), random.randint(1, 28))

# Create sample users
users = [
    User.objects.create_user(username=f'user{i}', password=f'password{i}', email=f'user{i}@example.com')
    for i in range(1, 11)
]

# Create sample organizers
organizers = [
    Organizer.objects.create(name=f'Travel Organizer {i}', contact_email=f'contact{i}@travelorganizer.com', contact_phone=f'12345{i}6789')
    for i in range(1, 6)
]

# Create sample places
places = [
    Place.objects.create(
        name=f'Place {i}',
        city=f'City {i}',
        state=f'State {i}',
        image=f'places/place{i}.jpg',
        famous_food=f'Famous Food {i}',
        featured=random.choice([True, False]),
        latitude=round(random.uniform(-90, 90), 4),
        longitude=round(random.uniform(-180, 180), 4),
        celebrated_festivals=f'Festival {i}',
        description=f'Description of place {i}.'
    )
    for i in range(1, 11)
]

# Create sample hotels
hotels = [
    Hotel.objects.create(
        name=f'Hotel {i}',
        image=f'hotels/hotel{i}.jpg',
        city=f'City {i}',
        state=f'State {i}'
    )
    for i in range(1, 11)
]

# Create sample trips
trips = []
for i in range(1, 6):
    trip = Trip.objects.create(
        organizer=random.choice(organizers),
        price=random.uniform(500, 5000),
        duration=random.randint(2, 10),
        transportation_medium=random.choice(['Bus', 'Train', 'Flight'])
    )
    # Associate random places and hotels with the trip
    trip.places.set(random.sample(places, random.randint(1, 3)))
    trip.hotel.set(random.sample(hotels, random.randint(1, 2)))
    trips.append(trip)

# Create sample reviews
for i in range(1, 21):
    Review.objects.create(
        user=random.choice(users),
        trip=random.choice(trips),
        rating=random.randint(1, 5),
        comment=f'This is review {i} comment. The trip was {"great" if i % 2 == 0 else "okay"}.'
    )

# Create sample bookings
for i in range(1, 21):
    booking = Booking.objects.create(
        user=random.choice(users),
        trip=random.choice(trips),
        booking_date=random_date(2024),
        num_people=random.randint(1, 5),
        total_cost=random.uniform(500, 5000)
    )

# Create sample place images
for place in places:
    for i in range(1, 3):  # Two images per place
        PlaceImage.objects.create(
            place=place,
            image=f'place_images/place_{place.id}_image{i}.jpg',
            caption=f'Image {i} for {place.name}'
        )

print("Extended sample data created successfully!")
