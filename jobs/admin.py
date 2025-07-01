from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'experience_level', 'posted_by', 'posted_date', 'is_active']
    list_filter = ['job_type', 'experience_level', 'is_active', 'posted_date']
    search_fields = ['title', 'company', 'location', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'posted_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'location', 'job_type', 'experience_level')
        }),
        ('Salary Information', {
            'fields': ('salary_min', 'salary_max'),
            'classes': ('collapse',)
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'benefits')
        }),
        ('Metadata', {
            'fields': ('posted_by', 'is_active'),
            'classes': ('collapse',)
        }),
    )
