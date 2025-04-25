from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"
    
class BusLine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route_id = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class SavedBusLine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_bus_lines")
    bus_line = models.ForeignKey(BusLine, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.bus_line.name}"

class Detour(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    affected_lines = models.ManyToManyField(BusLine, related_name='detours')
    
    def __str__(self):
        return self.title