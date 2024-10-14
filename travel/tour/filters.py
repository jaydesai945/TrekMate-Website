from django_filters import rest_framework as filters
from .models import Trip, Organizer

class TripFilter(filters.FilterSet):
    place_name = filters.CharFilter(method='filter_by_place_name')
    organizer_trips = filters.CharFilter(method='filter_by_organizer')
    place_id = filters.NumberFilter(field_name='places', lookup_expr='id')

    class Meta:
        model = Trip
        fields = ['place_name', 'organizer_trips', 'place_id']

    def filter_by_place_name(self, queryset, name, value):
        return queryset.filter(places__name__icontains=value).distinct()

    def filter_by_organizer(self, queryset, name, value):
        try:
            organizer = Organizer.objects.get(name__icontains=value)
            return queryset.filter(organizer=organizer).distinct()
        except Organizer.DoesNotExist:
            return queryset.none()
