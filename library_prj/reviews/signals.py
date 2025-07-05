from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from library_prj.books.models import Book
from django.db.models import Avg
from library_prj.users.models import Notification

@receiver(post_save, sender=Review)
def update_book_average_rating(sender, instance, created, **kwargs):
    # Calculer la note moyenne et l'enregistrer dans Book si besoin
    book = instance.book
    avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
    print(f"Note moyenne du livre '{book.title}': {avg_rating}")
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Votre avis sur le livre '{book.title}' a bien été pris en compte. Merci !",
            link=""
        )
    # Si tu veux stocker la moyenne dans Book, ajoute un champ average_rating dans Book
    # book.average_rating = avg_rating
    # book.save()
    pass 