from django.db import models

class Painter(models.Model):
    name = models.CharField(max_length=100)
