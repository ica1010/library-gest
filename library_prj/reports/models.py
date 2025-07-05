from django.db import models

# Create your models here.

class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Ventes'),
        ('loans', 'Emprunts'),
        ('stock', 'Stock'),
        ('custom', 'Personnalisé'),
    ]
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.date.date()}"
