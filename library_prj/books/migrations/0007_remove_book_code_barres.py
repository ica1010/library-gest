# Generated by Django 5.1.11 on 2025-07-05 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_book_auteurs_book_code_barres_book_collection_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="code_barres",
        ),
    ]
