from django.db import models
from django.conf import settings
from library_prj.books.models import Book

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expirée'), ('cancelled', 'Annulée')], default='active')

    def __str__(self):
        return f"{self.user} - {self.book}"
