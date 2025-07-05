from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from library_prj.reservations.models import Reservation
from library_prj.users.models import Notification
# from library_prj.reservations.models import Reservation  # Uncomment si besoin de notifications

@receiver(post_save, sender=Book)
def notify_reservations_on_book_update(sender, instance, created, **kwargs):
    # Notifier les utilisateurs si le stock passe de 0 à >0
    if not created:
        previous = Book.objects.get(pk=instance.pk)
        if previous.stock == 0 and instance.stock > 0:
            reservations = Reservation.objects.filter(book=instance, status='active')
            for reservation in reservations:
                Notification.objects.create(
                    user=reservation.user,
                    message=f"Le livre '{instance.title}' que vous avez réservé est maintenant disponible !",
                    link=""  # Tu peux ajouter un lien vers la fiche du livre
                )
                print(f"Notification: {reservation.user} - Le livre '{instance.title}' est maintenant disponible !")
    # Exemple : notifier les utilisateurs ayant réservé ce livre
    # reservations = Reservation.objects.filter(book=instance, status='active')
    # for reservation in reservations:
    #     # Envoyer une notification à reservation.user
    #     pass
    pass  # À compléter selon la logique de notification 