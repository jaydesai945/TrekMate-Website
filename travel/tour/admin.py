from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Organizer)
admin.site.register(models.Place)
admin.site.register(models.Hotel)
admin.site.register(models.Trip)
admin.site.register(models.Booking)
admin.site.register(models.Review)
admin.site.register(models.PlaceImage)