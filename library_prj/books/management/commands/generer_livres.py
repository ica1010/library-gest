from django.core.management.base import BaseCommand
from library_prj.books.factories import BookFactory

class Command(BaseCommand):
    help = "Génère des livres factices avec images"

    def add_arguments(self, parser):
        parser.add_argument('--nb', type=int, default=20, help='Nombre de livres à générer')

    def handle(self, *args, **options):
        nb = options['nb']
        for _ in range(nb):
            BookFactory()
        self.stdout.write(self.style.SUCCESS(f"{nb} livres générés avec succès !")) 