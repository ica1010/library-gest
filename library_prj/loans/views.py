from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Loan
from library_prj.books.models import Book

MAX_LOANS = 3  # Limite d'emprunts simultanés
LOAN_DURATION_DAYS = 14  # Durée d'un emprunt

@login_required
def loan_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Vérifier le stock
    if book.stock < 1:
        messages.error(request, "Ce livre n'est plus disponible.")
        return redirect('books:detail', pk=book_id)
    # Vérifier la limite d'emprunts
    active_loans = Loan.objects.filter(user=request.user, status='ongoing').count()
    if active_loans >= MAX_LOANS:
        messages.error(request, f"Vous avez atteint la limite de {MAX_LOANS} emprunts simultanés.")
        return redirect('books:detail', pk=book_id)
    # Vérifier si l'utilisateur a déjà un emprunt actif pour ce livre
    if Loan.objects.filter(user=request.user, book=book, status='ongoing').exists():
        messages.warning(request, "Vous avez déjà emprunté ce livre.")
        return redirect('books:detail', pk=book_id)
    # Créer l'emprunt
    due_date = timezone.now().date() + timedelta(days=LOAN_DURATION_DAYS)
    Loan.objects.create(user=request.user, book=book, due_date=due_date)
    # Décrémenter le stock
    book.stock = max(0, book.stock - 1)
    book.save()
    messages.success(request, f"Vous avez emprunté '{book.title}' jusqu'au {due_date.strftime('%d/%m/%Y')}.")
    return redirect('loans:my_loans')

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user).select_related('book').order_by('-loan_date')
    return render(request, 'loans/my_loans.html', {'loans': loans})
