from django.db import models


class Guest(models.Model):
    username = "Guest User"

    def __str__(self):
        return self.username
