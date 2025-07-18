# Generated by Django 5.2.4 on 2025-07-04 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("biography", models.TextField(blank=True)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("nationality", models.CharField(blank=True, max_length=100)),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="authors/"),
                ),
            ],
        ),
    ]
