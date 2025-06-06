from django.db import models


class Authenticated(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self
