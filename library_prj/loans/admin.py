from django.contrib import admin
from .models import Loan, Penalty

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'loan_date', 'due_date', 'return_date', 'status')
    list_filter = ('status', 'loan_date', 'due_date')
    search_fields = ('user__username', 'book__title')

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reason', 'date')
    list_filter = ('date',)
    search_fields = ('user__username', 'reason')
