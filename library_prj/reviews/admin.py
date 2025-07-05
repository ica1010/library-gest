from django.contrib import admin
from .models import Review, Recommendation
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'date', 'is_approved', 'view_link')
    list_filter = ('rating', 'date', 'is_approved')
    search_fields = ('user__username', 'book__title')
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} avis validés.")
    approve_reviews.short_description = "Valider les avis sélectionnés"

    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} avis refusés.")
    reject_reviews.short_description = "Refuser les avis sélectionnés"

    def view_link(self, obj):
        url = reverse('admin:reviews_review_change', args=[obj.id])
        return format_html('<a href="{}">Voir</a>', url)
    view_link.short_description = 'Détail'

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'score')
    search_fields = ('user__username', 'book__title')
