from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'date')
    list_filter = ('report_type', 'date')
    search_fields = ('report_type',)
