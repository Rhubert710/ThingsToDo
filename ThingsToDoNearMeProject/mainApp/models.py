from django.db import models


class Event(models.Model):

    title = models.CharField(max_length=200)
    Description = models.CharField(max_length=200)
    date = models.DateField()
    # Day_of_week = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Flyer = models.ForeignKey(Flyer, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(auto_now_add=True)
