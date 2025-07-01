from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date', 'updated_date']
    list_filter = ['status', 'applied_date', 'job__company']
    search_fields = ['applicant__email', 'applicant__username', 'job__title', 'job__company']
    date_hierarchy = 'applied_date'
    list_editable = ['status']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'applicant', 'resume', 'cover_letter')
        }),
        ('Status Information', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('applied_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['applied_date', 'updated_date']
