from django.contrib import admin
from .models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience, 
    TechnicalSkill, Education, Technology, Project, 
    Certification, Award, Language
)

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'format_type', 'version', 'is_active', 'created_at']
    list_filter = ['format_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template', 'language', 'visibility', 'last_modified']
    list_filter = ['visibility', 'language', 'template', 'created_at']
    search_fields = ['title', 'user__email', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ['resume', 'section_type', 'title', 'order', 'is_visible']
    list_filter = ['section_type', 'is_visible']
    search_fields = ['title', 'resume__title']
    list_editable = ['order', 'is_visible']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'resume', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date', 'company']
    search_fields = ['job_title', 'company', 'resume__title']
    date_hierarchy = 'start_date'
    filter_horizontal = ['technologies']

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ['technology', 'resume', 'proficiency', 'years_experience', 'is_visible']
    list_filter = ['proficiency', 'is_visible', 'technology__category']
    search_fields = ['technology__name', 'resume__title']
    list_editable = ['proficiency', 'is_visible']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'resume', 'start_date', 'end_date', 'gpa']
    list_filter = ['start_date', 'end_date']
    search_fields = ['degree', 'institution', 'resume__title']
    date_hierarchy = 'end_date'

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'role', 'resume', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'role', 'resume__title']
    date_hierarchy = 'start_date'
    filter_horizontal = ['technologies']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'resume', 'issue_date', 'expiration_date']
    list_filter = ['issue_date', 'expiration_date']
    search_fields = ['name', 'issuer', 'resume__title']
    date_hierarchy = 'issue_date'
    filter_horizontal = ['skills']

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'resume', 'category', 'issue_date', 'is_visible']
    list_filter = ['category', 'is_visible', 'issue_date']
    search_fields = ['title', 'issuer', 'resume__title']
    date_hierarchy = 'issue_date'
    list_editable = ['is_visible']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'resume', 'proficiency', 'certification', 'is_visible']
    list_filter = ['proficiency', 'is_visible']
    search_fields = ['name', 'resume__title']
    list_editable = ['is_visible']
