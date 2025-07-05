from django.db import models

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
