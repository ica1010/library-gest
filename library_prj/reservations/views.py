from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Reservation
from library_prj.books.models import Book
from datetime import timedelta

# Create your views here.

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Vérifier si une réservation active existe déjà pour ce livre et cet utilisateur
    existing = Reservation.objects.filter(user=request.user, book=book, status='active').exists()
    if existing:
        messages.warning(request, "Vous avez déjà réservé ce livre.")
        return redirect('books:detail', pk=book_id)
    # Créer la réservation (expiration par défaut à +7 jours)
    expiration = timezone.now().date() + timedelta(days=7)
    Reservation.objects.create(user=request.user, book=book, expiration_date=expiration)
    messages.success(request, "Votre réservation a bien été enregistrée.")
    return redirect('books:detail', pk=book_id)

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})
