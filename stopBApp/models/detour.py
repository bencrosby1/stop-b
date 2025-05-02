from django.db import models
from .busline import BusLine

class Detour(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    affected_lines = models.ManyToManyField(BusLine, related_name='detours')
    
    def __str__(self):
        return self.title