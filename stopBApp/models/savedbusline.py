from django.db import models
from django.contrib.auth.models import User
from .busline import BusLine

class SavedBusLine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_bus_lines")
    bus_line = models.ForeignKey(BusLine, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.bus_line.name}"