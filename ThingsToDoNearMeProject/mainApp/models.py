from django.db import models
from django.utils import timezone


class Event(models.Model):

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    # Day_of_week = models.CharField(max_length=10)
    address = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # Flyer = models.ForeignKey(Flyer, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(auto_now_add=True)
