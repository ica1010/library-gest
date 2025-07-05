from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path('', views.book_list_view, name='list'),
    path('categories/', views.category_list_view, name='categories'),
    path('genres/', views.genre_list_view, name='genres'),

    # admin
    path('admin-list/', views.book_admin_list_view, name='admin_list'),
    path('admin-categories/', views.category_admin_list_view, name='admin_categories'),
    path('admin-categories/edit/<int:category_id>/', views.admin_edit_category_view, name='admin_edit_category'),
    path('admin-categories/delete/<int:category_id>/', views.admin_delete_category_view, name='admin_delete_category'),
    path('admin-genres/edit/<int:genre_id>/', views.admin_edit_genre_view, name='admin_edit_genre'),
    path('admin-genres/delete/<int:genre_id>/', views.admin_delete_genre_view, name='admin_delete_genre'),
    path('add/', views.book_create_view, name='add'),
    path('admin-add/', views.admin_add_book_view, name='admin_add'),
    path('admin-edit/<int:book_id>/', views.admin_edit_book_view, name='admin_edit'),
    path('admin-delete/<int:book_id>/', views.admin_delete_book_view, name='admin_delete'),
    path('admin-restore/<int:book_id>/', views.admin_restore_book_view, name='admin_restore'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('search/', views.search_books_view, name='search'),
    path('categorie/<int:pk>/', views.category_books, name='category_books'),
    path('genre/<int:pk>/', views.genre_books, name='genre_books'),
    path('admin-loans/', views.admin_loan_list, name='admin_loan_list'),
    path('admin-sales/', views.admin_sale_list, name='admin_sale_list'),
    path('admin-loans/action/<int:loan_id>/', views.admin_loan_action, name='admin_loan_action'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-reviews/', views.admin_reviews_list_view, name='admin_reviews_list'),
    path('admin-reviews/update-status/<int:review_id>/', views.admin_review_update_status, name='admin_review_update_status'),
]
