from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Book, Category, Genre
from .forms import BookForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from library_prj.loans.models import Loan
from library_prj.sales.models import Sale
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
import json
import calendar
from library_prj.reviews.models import Review
from django.db.models import Avg
from django.core.paginator import Paginator
from django.db.models import Avg
from library_prj.authors.models import Author
from library_prj.publishers.models import Publisher

def book_list_view(request):
    books = Book.objects.all()
    q = request.GET.get('q')
    if q:
        books = books.filter(title__icontains=q) | books.filter(summary__icontains=q)
    return render(request, "books/book_list.html", {"books": books, "q": q})

def category_list_view(request):
    categories = Category.objects.all()
    return render(request, "books/category_list.html", {"categories": categories})

def book_create_view(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/books/")
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form})

@staff_member_required
def book_admin_list_view(request):
    books = Book.objects.filter(is_deleted=False)
    categories = Category.objects.all()
    genres = Genre.objects.all()
    languages = [
        'Français', 'Anglais', 'Espagnol', 'Allemand', 'Italien', 'Portugais', 'Arabe', 'Chinois', 'Japonais', 'Russe'
    ]
    auteurs = Author.objects.all()
    editeurs = Publisher.objects.all()
    return render(request, "admin/book_list.html", {
        "books": books,
        "categories": categories,
        "genres": genres,
        "languages": languages,
        "auteurs": auteurs,
        "editeurs": editeurs,
    })

@staff_member_required
def category_admin_list_view(request):
    categories = Category.objects.all()
    genres = Genre.objects.all()
    return render(request, "admin/category_list.html", {"categories": categories, "genres": genres})

@staff_member_required
def admin_add_book_view(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            isbn = request.POST.get("isbn")
            stock = request.POST.get("stock")
            price = request.POST.get("price")
            publication_date = request.POST.get("publication_date")
            pages = request.POST.get("pages")
            summary = request.POST.get("summary")
            language = request.POST.get("language")
            format_ = request.POST.get("format")
            dimensions = request.POST.get("dimensions")
            poids = request.POST.get("poids")
            code_barres = request.POST.get("code_barres")
            illustrateur = request.POST.get("illustrateur")
            collection = request.POST.get("collection")
            niveau_scolaire = request.POST.get("niveau_scolaire")
            public_cible = request.POST.get("public_cible")
            editeur_id = request.POST.get("editeur")
            auteurs_ids = request.POST.getlist("auteurs")
            categories = request.POST.getlist("categories")
            genres = request.POST.getlist("genres")
            cover_front = request.FILES.get("cover_front")
            cover_back = request.FILES.get("cover_back")

            if not title or not isbn:
                messages.error(request, "Le titre et l'ISBN sont obligatoires.")
                return HttpResponseRedirect(reverse("books:admin_list"))

            if Book.objects.filter(isbn=isbn).exists():
                messages.error(request, "Un livre avec cet ISBN existe déjà. Veuillez saisir un ISBN unique.")
                return HttpResponseRedirect(reverse("books:admin_list"))

            book = Book.objects.create(
                title=title,
                isbn=isbn,
                stock=stock or 0,
                price=price or 0,
                publication_date=publication_date or None,
                pages=pages or None,
                summary=summary or "",
                language=language or "",
                format=format_ or "",
                dimensions=dimensions or "",
                poids=poids or None,
                code_barres=code_barres or "",
                illustrateur=illustrateur or "",
                collection=collection or "",
                niveau_scolaire=niveau_scolaire or "",
                public_cible=public_cible or "",
                cover_front=cover_front,
                cover_back=cover_back,
                editeur=Publisher.objects.get(pk=editeur_id) if editeur_id else None,
            )

            if auteurs_ids:
                book.auteurs.set(Author.objects.filter(pk__in=auteurs_ids))
            category_objs = []
            for cat in categories:
                try:
                    cat_obj = Category.objects.get(pk=int(cat))
                except (ValueError, Category.DoesNotExist):
                    cat_obj, _ = Category.objects.get_or_create(name=cat)
                category_objs.append(cat_obj)
            book.categories.set(category_objs)
            genre_objs = []
            for gen in genres:
                try:
                    gen_obj = Genre.objects.get(pk=int(gen))
                except (ValueError, Genre.DoesNotExist):
                    gen_obj, _ = Genre.objects.get_or_create(name=gen)
                genre_objs.append(gen_obj)
            book.genres.set(genre_objs)

            messages.success(request, "Le livre a bien été créé.")
            return HttpResponseRedirect(reverse("books:admin_list"))
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du livre : {str(e)}")
            return HttpResponseRedirect(reverse("books:admin_list"))
    return HttpResponseRedirect(reverse("books:admin_list"))

@staff_member_required
def admin_edit_book_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.isbn = request.POST.get("isbn")
        book.stock = request.POST.get("stock")
        book.price = request.POST.get("price") or 0
        book.publication_date = request.POST.get("publication_date") or None
        book.pages = request.POST.get("pages") or None
        book.summary = request.POST.get("summary")
        book.language = request.POST.get("language")
        book.format = request.POST.get("format")
        book.dimensions = request.POST.get("dimensions")
        book.poids = request.POST.get("poids") or None
        book.code_barres = request.POST.get("code_barres")
        book.illustrateur = request.POST.get("illustrateur")
        book.collection = request.POST.get("collection")
        book.niveau_scolaire = request.POST.get("niveau_scolaire")
        book.public_cible = request.POST.get("public_cible")
        editeur_id = request.POST.get("editeur")
        book.editeur = Publisher.objects.get(pk=editeur_id) if editeur_id else None
        # Images
        if request.FILES.get("cover_front"):
            book.cover_front = request.FILES.get("cover_front")
        if request.FILES.get("cover_back"):
            book.cover_back = request.FILES.get("cover_back")
        # ManyToMany
        auteurs_ids = request.POST.getlist("auteurs")
        if auteurs_ids:
            book.auteurs.set(Author.objects.filter(pk__in=auteurs_ids))
        else:
            book.auteurs.clear()
        categories = request.POST.getlist("categories")
        category_objs = []
        for cat in categories:
            try:
                cat_obj = Category.objects.get(pk=int(cat))
            except (ValueError, Category.DoesNotExist):
                cat_obj, _ = Category.objects.get_or_create(name=cat)
            category_objs.append(cat_obj)
        book.categories.set(category_objs)
        genres = request.POST.getlist("genres")
        genre_objs = []
        for gen in genres:
            try:
                gen_obj = Genre.objects.get(pk=int(gen))
            except (ValueError, Genre.DoesNotExist):
                gen_obj, _ = Genre.objects.get_or_create(name=gen)
            genre_objs.append(gen_obj)
        book.genres.set(genre_objs)
        book.save()
        messages.success(request, "Livre modifié avec succès.")
        return HttpResponseRedirect(reverse("books:admin_list"))
    # Préparer les catégories/genres pour le formulaire
    categories = Category.objects.all()
    genres = Genre.objects.all()
    languages = [
        'Français', 'Anglais', 'Espagnol', 'Allemand', 'Italien', 'Portugais', 'Arabe', 'Chinois', 'Japonais', 'Russe'
    ]
    auteurs = Author.objects.all()
    editeurs = Publisher.objects.all()
    return render(request, "admin/book_edit.html", {
        "book": book,
        "categories": categories,
        "genres": genres,
        "languages": languages,
        "auteurs": auteurs,
        "editeurs": editeurs,
    })

@staff_member_required
def admin_delete_book_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_deleted = True
    book.save()
    messages.success(request, "Livre supprimé (corbeille).")
    return HttpResponseRedirect(reverse("books:admin_list"))

@staff_member_required
def admin_restore_book_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_deleted = False
    book.save()
    messages.success(request, "Livre restauré.")
    return HttpResponseRedirect(reverse("books:admin_list"))

@staff_member_required
def admin_edit_category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.description = request.POST.get("description")
        if request.FILES.get("image"):
            category.image = request.FILES["image"]
        category.save()
        messages.success(request, "Catégorie modifiée avec succès.")
        return redirect('books:admin_categories')
    return render(request, "admin/category_edit.html", {"category": category})

@staff_member_required
def admin_delete_category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, "Catégorie supprimée.")
    return redirect('books:admin_categories')

@staff_member_required
def admin_edit_genre_view(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    if request.method == "POST":
        genre.name = request.POST.get("name")
        genre.description = request.POST.get("description")
        genre.save()
        messages.success(request, "Genre modifié avec succès.")
        return redirect('books:admin_categories')
    return render(request, "admin/genre_edit.html", {"genre": genre})

@staff_member_required
def admin_delete_genre_view(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    genre.delete()
    messages.success(request, "Genre supprimé.")
    return redirect('books:admin_categories')

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    has_active_loan = False
    can_review = False
    user_has_reviewed = False
    avg_rating = None
    reviews = Review.objects.filter(book=book, is_approved=True).select_related('user').order_by('-date')
    if reviews.exists():
        avg_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)
    if request.user.is_authenticated:
        has_active_loan = Loan.objects.filter(user=request.user, book=book, status='ongoing').exists()
        has_bought = Sale.objects.filter(user=request.user, items__book=book, status='completed').exists()
        can_review = has_active_loan or has_bought
        user_has_reviewed = Review.objects.filter(user=request.user, book=book).exists()
        if request.method == 'POST' and can_review and not user_has_reviewed:
            rating = int(request.POST.get('rating', 0))
            comment = request.POST.get('comment', '').strip()
            if 1 <= rating <= 5:
                Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
                messages.success(request, "Votre avis a bien été soumis et sera publié après validation.")
                return redirect('books:detail', pk=book.pk)
            else:
                messages.error(request, "Merci de donner une note entre 1 et 5.")
    return render(request, 'books/book_detail.html', {
        'book': book,
        'has_active_loan': has_active_loan,
        'can_review': can_review,
        'user_has_reviewed': user_has_reviewed,
        'avg_rating': avg_rating,
        'reviews': reviews,
        'star_range': range(1, 6),
    })

def genre_list_view(request):
    genres = Genre.objects.all()
    return render(request, "books/genre_list.html", {"genres": genres})

def search_books_view(request):
    books = Book.objects.all()
    q = request.GET.get('q')
    category = request.GET.get('category')
    genre = request.GET.get('genre')
    language = request.GET.get('language')
    prix_max = request.GET.get('prix_max')
    if q:
        books = books.filter(Q(title__icontains=q) | Q(summary__icontains=q))
    if category:
        books = books.filter(categories__id=category)
    if genre:
        books = books.filter(genres__id=genre)
    if language:
        books = books.filter(language__icontains=language)
    if prix_max:
        books = books.filter(price__lte=prix_max)
    books = books.distinct()
    categories = Category.objects.all()
    genres = Genre.objects.all()
    return render(request, "books/search_results.html", {
        "books": books,
        "q": q,
        "categories": categories,
        "genres": genres,
    })

def category_books(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(categories=category)
    return render(request, 'books/category_books.html', {'category': category, 'books': books})

def genre_books(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.filter(genres=genre)
    return render(request, 'books/genre_books.html', {'genre': genre, 'books': books})

@staff_member_required
def admin_loan_list(request):
    loans = Loan.objects.all().select_related('user', 'book')
    return render(request, 'admin/loan_list.html', {'loans': loans})

@staff_member_required
def admin_sale_list(request):
    sales = Sale.objects.all().select_related('user')
    return render(request, 'admin/sale_list.html', {'sales': sales})

@staff_member_required
@require_POST
def admin_loan_action(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    action = request.POST.get('action')
    if action == 'validate' and loan.status != 'ongoing':
        loan.status = 'ongoing'
        loan.loan_date = timezone.now().date()
        loan.save()
        messages.success(request, "Emprunt validé.")
    elif action == 'refuse' and loan.status != 'refused':
        loan.status = 'refused'
        loan.save()
        messages.success(request, "Emprunt refusé.")
    elif action == 'return' and loan.status in ['ongoing', 'late']:
        loan.status = 'returned'
        loan.return_date = timezone.now().date()
        loan.save()
        messages.success(request, "Retour validé.")
    else:
        messages.warning(request, "Action non autorisée ou déjà effectuée.")
    return redirect('books:admin_loan_list')

@staff_member_required
def admin_dashboard(request):
    User = get_user_model()
    stats = {
        'books': Book.objects.count(),
        'loans_ongoing': Loan.objects.filter(status='ongoing').count(),
        'loans_late': Loan.objects.filter(status='late').count(),
        'sales': Sale.objects.count(),
        'sales_pending': Sale.objects.filter(status='pending').count(),
        'users': User.objects.count(),
    }
    # Top 5 livres les plus empruntés
    top_books = Book.objects.annotate(nb=Count('loan')).order_by('-nb')[:5]
    # Derniers emprunts
    last_loans = Loan.objects.select_related('user', 'book').order_by('-loan_date')[:5]
    # Dernières commandes
    last_sales = Sale.objects.select_related('user').order_by('-date')[:5]
    # Derniers avis
    last_reviews = Review.objects.select_related('user', 'book').order_by('-date')[:20]
    # Générer les labels et données pour les 12 derniers mois
    now = timezone.now()
    labels = []
    data = []
    for i in range(11, -1, -1):
        month = (now - timezone.timedelta(days=30*i)).month
        year = (now - timezone.timedelta(days=30*i)).year
        labels.append(f"{calendar.month_abbr[month]} {year}")
        count = Loan.objects.filter(loan_date__year=year, loan_date__month=month).count()
        data.append(count)
    return render(request, 'admin/dashboard.html', {
        'stats': stats,
        'top_books': top_books,
        'last_loans': last_loans,
        'last_sales': last_sales,
        'last_reviews': last_reviews,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    })

@staff_member_required
def admin_reviews_list_view(request):
    reviews = Review.objects.select_related('user', 'book').order_by('-date')
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/review_list.html', {
        'page_obj': page_obj,
    })

@staff_member_required
@require_POST
def admin_review_update_status(request, review_id):
    review = Review.objects.get(pk=review_id)
    action = request.POST.get('action')
    if action == 'approve':
        review.is_approved = True
        review.save()
        messages.success(request, "Avis validé.")
    elif action == 'reject':
        review.is_approved = False
        review.save()
        messages.success(request, "Avis refusé.")
    else:
        messages.error(request, "Action inconnue.")
    next_url = request.POST.get('next', '') or request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

def home_view(request):
    from library_prj.books.models import Book
    from library_prj.reviews.models import Review
    books = Book.objects.all()[:12]  # ou filtrer les populaires
    # Calculer la note moyenne pour chaque livre
    for book in books:
        avg = Review.objects.filter(book=book, is_approved=True).aggregate(models.Avg('rating'))['rating__avg']
        book.avg_rating = round(avg, 1) if avg else None
    categories = Category.objects.all()
    genres = Genre.objects.all()
    return render(request, 'pages/home.html', {
        'books': books,
        'categories': categories,
        'genres': genres,
        'star_range': range(1, 6),
    })
