from django.db import models
from django.conf import settings
from library_prj.books.models import Book

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="Avis validé")

    def __str__(self):
        return f"{self.user} - {self.book} ({self.rating}/5)"

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.user} -> {self.book} ({self.score})"
