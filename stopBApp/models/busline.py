from django.db import models

class BusLine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route_id = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name