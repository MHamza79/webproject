# resume_builder/forms.py
from django import forms
from .models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)

class ResumeTemplateForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplate
        fields = ['name', 'description', 'format_type', 'version']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'slug', 'summary', 'tags', 'template', 'language', 'visibility']

class ResumeSectionForm(forms.ModelForm):
    class Meta:
        model = ResumeSection
        fields = ['section_type', 'title', 'content', 'order', 'is_visible']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description', 'achievements', 'technologies']

class TechnicalSkillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['technology', 'proficiency', 'years_experience', 'last_used', 'project_count', 'is_visible']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'location', 'start_date', 'end_date', 'gpa', 'description', 'is_visible']

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'category', 'icon']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'role', 'start_date', 'end_date', 'description', 'technologies', 'outcomes', 'url', 'is_active']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'issue_date', 'expiration_date', 'credential_id', 'verification_url', 'skills']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'issuer', 'issue_date', 'category', 'description', 'impact_metrics', 'is_visible']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency', 'certification', 'is_visible']

class ResumeTemplateSelectionForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['template']