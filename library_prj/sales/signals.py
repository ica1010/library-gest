from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaleItem
from library_prj.users.models import Notification

@receiver(post_save, sender=SaleItem)
def decrease_book_stock_on_sale(sender, instance, created, **kwargs):
    if created:
        instance.book.stock = max(0, instance.book.stock - instance.quantity)
        instance.book.save()
        Notification.objects.create(
            user=instance.sale.user,
            message=f"Vous avez acheté {instance.quantity} exemplaire(s) du livre '{instance.book.title}'. Merci pour votre achat !",
            amount=instance.unit_price * instance.quantity,
            link=""
        )
        print(f"Vente: Stock du livre '{instance.book.title}' diminué à {instance.book.stock}") 