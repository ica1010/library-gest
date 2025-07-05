from .models import Category, Genre
from django.db.models import Count

def top_categories_and_genres(request):
    # Top 5 catégories par nombre de livres associés
    top_categories = Category.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
    # Top 5 genres par nombre de livres associés
    top_genres = Genre.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
    return {
        'top_categories': top_categories,
        'top_genres': top_genres,
    } 