from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('book/<int:book_id>/loan/', views.loan_book, name='loan_book'),
    path('mes-emprunts/', views.my_loans, name='my_loans'),
    # (à compléter : mes emprunts, retour, etc.)
] 