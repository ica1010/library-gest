from django.shortcuts import render, redirect
from library_prj.books.models import Category, Book, Genre
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from library_prj.reviews.models import Review

def home(request):
    categories = Category.objects.all()
    books = Book.objects.filter(is_deleted=False)[:12]
    genres = Genre.objects.all()
    return render(request, "pages/home.html", {"categories": categories, "books": books, "genres": genres})

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('users:admin_dashboard')  # dashboard/admin/
    from library_prj.loans.models import Loan
    from library_prj.reservations.models import Reservation
    from library_prj.sales.models import Cart
    loans_count = Loan.objects.filter(user=request.user, status='ongoing').count()
    reservations_count = Reservation.objects.filter(user=request.user, status='active').count()
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
    # Livres à afficher (8 premiers)
    books = Book.objects.all()[:8]
    for book in books:
        avg = Review.objects.filter(book=book, is_approved=True).aggregate(Avg('rating'))['rating__avg']
        book.avg_rating = round(avg, 1) if avg else None
    return render(request, "users/dashboard.html", {
        "loans_count": loans_count,
        "reservations_count": reservations_count,
        "cart_count": cart_count,
        "books": books,
        "star_range": range(1, 6),
    })

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('users:dashboard')
    return render(request, "admin/dashboard.html") 