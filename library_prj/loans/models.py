from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from library_prj.books.models import Book

class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ongoing', 'En cours'), ('returned', 'Rendu'), ('late', 'En retard')], default='ongoing')

    def __str__(self):
        return f"{self.user} - {self.book}"

class Penalty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=10, decimal_places=0, default_currency='XOF')
    reason = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"
