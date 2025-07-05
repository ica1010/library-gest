from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from library_prj.books.models import Book

# Create your models here.

class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = MoneyField(max_digits=10, decimal_places=0, default_currency='XOF')
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('completed', 'Complétée'), ('cancelled', 'Annulée')], default='pending')
    status_paiement = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('paid', 'Payé'),
            ('failed', 'Échoué'),
            ('refunded', 'Remboursé'),
        ],
        default='pending'
    )
    adresse_livraison = models.CharField(max_length=255, blank=True, null=True)
    adresse_facturation = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    mode_paiement = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True)
    livraison_statut = models.CharField(max_length=30, choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('livre', 'Livré'), ('annule', 'Annulé')], default='en_attente')

    def __str__(self):
        return f"Vente #{self.id} - {self.date.date()}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = MoneyField(max_digits=10, decimal_places=0, default_currency='XOF')

    def __str__(self):
        return f"{self.book} x{self.quantity}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book} x{self.quantity}"
