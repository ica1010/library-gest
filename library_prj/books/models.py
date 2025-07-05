from django.db import models
from djmoney.models.fields import MoneyField
from library_prj.authors.models import Author
from library_prj.publishers.models import Publisher

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    cover_front = models.ImageField(upload_to='books/covers/front/', blank=True, null=True)
    cover_back = models.ImageField(upload_to='books/covers/back/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    is_deleted = models.BooleanField(default=False)
    price = MoneyField(max_digits=10, decimal_places=0, default_currency='XOF', default=0)
    auteurs = models.ManyToManyField(Author, blank=True, related_name='books')
    editeur = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    format = models.CharField(max_length=50, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    poids = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    illustrateur = models.CharField(max_length=100, blank=True)
    collection = models.CharField(max_length=100, blank=True)
    niveau_scolaire = models.CharField(max_length=50, blank=True)
    public_cible = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title
