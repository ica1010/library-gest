from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from django.utils import timezone

@receiver(post_save, sender=Reservation)
def notify_user_on_reservation(sender, instance, created, **kwargs):
    if created:
        print(f"Confirmation: {instance.user} - Votre réservation du livre '{instance.book.title}' est enregistrée.")
    elif instance.status == 'expired':
        print(f"Notification: {instance.user} - Votre réservation du livre '{instance.book.title}' a expiré.")

@receiver(post_save, sender=Reservation)
def update_reservation_status(sender, instance, **kwargs):
    # Si la réservation est active et la date d'expiration est passée, on la passe à 'expired'
    if instance.status == 'active' and instance.expiration_date < timezone.now().date():
        instance.status = 'expired'
        instance.save(update_fields=['status']) 