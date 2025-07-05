from django.contrib import admin
from .models import Publisher

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'contact')
    search_fields = ('name', 'website', 'contact')
