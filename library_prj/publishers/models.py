from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
