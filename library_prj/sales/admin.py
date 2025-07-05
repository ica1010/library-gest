from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username',)
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'book', 'quantity', 'unit_price')
    search_fields = ('book__title',)
