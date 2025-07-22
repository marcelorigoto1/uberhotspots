from django.db import models

class Pickup(models.Model):
    datetime = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    base = models.CharField(max_length=10)
    hour = models.IntegerField()
    weekday = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.datetime} - {self.lat}, {self.lon}"
