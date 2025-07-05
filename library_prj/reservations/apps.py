from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library_prj.reservations'

    def ready(self):
        import library_prj.reservations.signals
