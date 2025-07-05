from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, Penalty
from library_prj.books.models import Book
from django.utils import timezone
from library_prj.users.models import Notification

@receiver(post_save, sender=Loan)
def update_book_stock_on_loan(sender, instance, created, **kwargs):
    if created:
        # Diminuer le stock lors d'un nouvel emprunt
        instance.book.stock = max(0, instance.book.stock - 1)
        instance.book.save()
        print(f"Stock du livre '{instance.book.title}' diminué à {instance.book.stock}")
    elif instance.return_date:
        # Augmenter le stock lors du retour
        instance.book.stock += 1
        instance.book.save()
        print(f"Stock du livre '{instance.book.title}' augmenté à {instance.book.stock}")
    # Notifier en cas de retard (exemple)
    if instance.due_date < timezone.now().date() and not instance.return_date:
        Notification.objects.create(
            user=instance.user,
            message=f"Votre emprunt du livre '{instance.book.title}' est en retard !",
            link=""
        )
        print(f"Rappel: {instance.user} - L'emprunt du livre '{instance.book.title}' est en retard !")

@receiver(post_save, sender=Penalty)
def notify_user_on_penalty(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Vous avez une pénalité de {instance.amount} pour {instance.reason}",
            amount=instance.amount,
            link=""
        )
        print(f"Notification: {instance.user} - Vous avez une pénalité de {instance.amount} pour {instance.reason}") 