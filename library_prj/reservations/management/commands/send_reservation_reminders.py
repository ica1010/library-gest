from django.core.management.base import BaseCommand
from django.utils import timezone
from library_prj.reservations.models import Reservation

class Command(BaseCommand):
    help = "Envoie un rappel aux utilisateurs dont la réservation expire demain."

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        reservations = Reservation.objects.filter(expiration_date=tomorrow, status='active')
        for reservation in reservations:
            self.stdout.write(self.style.SUCCESS(
                f"Rappel: {reservation.user} - Votre réservation du livre '{reservation.book.title}' expire demain ({reservation.expiration_date}) !"
            )) 