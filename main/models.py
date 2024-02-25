from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()