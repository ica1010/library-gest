from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('book/<int:book_id>/reserve/', views.reserve_book, name='reserve_book'),
    path('mes-reservations/', views.my_reservations, name='my_reservations'),
] 