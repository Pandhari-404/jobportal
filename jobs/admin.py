"""
jobs/admin.py
=============
Register all models with the Django admin site.
Provides rich list displays, filters, and search.
"""

from django.contrib import admin
from .models import Job, Application, SavedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ('title', 'company', 'location', 'job_type', 'category', 'recruiter', 'posted_at', 'is_active')
    list_filter   = ('job_type', 'category', 'is_active', 'posted_at')
    search_fields = ('title', 'company', 'location', 'description')
    list_editable = ('is_active',)
    ordering      = ('-posted_at',)
    date_hierarchy = 'posted_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'company', 'logo', 'location', 'job_type', 'category', 'salary')
        }),
        ('Details', {
            'fields': ('description', 'requirements')
        }),
        ('Meta', {
            'fields': ('recruiter', 'is_active', 'posted_at')
        }),
    )
    readonly_fields = ('posted_at',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ('applicant', 'job', 'status', 'applied_at')
    list_filter   = ('status', 'applied_at')
    search_fields = ('applicant__email', 'applicant__first_name', 'job__title', 'job__company')
    ordering      = ('-applied_at',)
    list_editable = ('status',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display  = ('user', 'job', 'saved_at')
    search_fields = ('user__email', 'job__title')
    ordering      = ('-saved_at',)
