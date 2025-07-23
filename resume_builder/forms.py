# resume_builder/forms.py
from django import forms
from django.forms import DateInput
import json
from .models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)

class DatePickerInput(DateInput):
    input_type = 'date'

class JSONFieldWidget(forms.Textarea):
    """Custom widget for JSON fields that handles conversion between text and JSON"""
    
    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, (list, dict)):
            # Always return a string for rendering
            if isinstance(value, list):
                # Render as lines for user-friendly editing
                return '\n'.join(str(v) for v in value)
            return json.dumps(value, indent=2)
        return str(value)
    
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if not value:
            return []
        # PATCH: If value is already a list, join as string for rendering
        if isinstance(value, list):
            return '\n'.join(str(v) for v in value)
        try:
            # Handle both list and dict formats
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                # Convert dict to list if it's meant to be a list
                return [parsed] if parsed else []
            return parsed if isinstance(parsed, list) else [parsed]
        except Exception:
            # If JSON parsing fails, treat as plain text and split by lines
            lines = [line.strip() for line in value.split('\n') if line.strip()]
            return lines

class ResumeTemplateForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplate
        fields = ['name', 'description', 'format_type', 'version']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'format_type': forms.Select(attrs={'class': 'form-select'}),
            'version': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'slug', 'summary', 'tags', 'template', 'visibility', 'github_url', 'linkedin_url', 'location', 'phone', 'professional_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
            'template': forms.Select(attrs={'class': 'form-select'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourprofile'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'professional_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Professional Email'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Tags
        if self.instance and self.instance.pk and self.instance.tags:
            if isinstance(self.instance.tags, list):
                self.initial['tags'] = ', '.join(self.instance.tags)
        # Template choices
        template_qs = ResumeTemplate.objects.all()
        if template_qs.exists():
            self.fields['template'].queryset = template_qs
            self.fields['template'].empty_label = "Select template"
            self.fields['template'].required = True
            self.fields['template'].widget.attrs.pop('disabled', None)
        else:
            self.fields['template'].queryset = template_qs
            self.fields['template'].empty_label = "No templates available - Contact admin"
            self.fields['template'].required = False
            self.fields['template'].widget.attrs['disabled'] = 'disabled'
        # Visibility choices
        visibility_choices = [
            ('', 'Select visibility'),
            ('PRIVATE', 'Private'),
            ('PUBLIC', 'Public'),
            ('SHARED', 'Shared with Link'),
        ]
        self.fields['visibility'].choices = visibility_choices

class ResumeSectionForm(forms.ModelForm):
    class Meta:
        model = ResumeSection
        fields = ['section_type', 'title', 'content', 'order', 'is_visible']
        widgets = {
            'section_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class WorkExperienceForm(forms.ModelForm):
    new_technologies = forms.CharField(
        required=False,
        label='Technologies & Achievements (comma-separated or free text)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, React, AWS, Improved app performance by 30%', 'rows': 3})
    )
    class Meta:
        model = WorkExperience
        fields = ['resume', 'job_title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description', 'new_technologies']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': DatePickerInput(attrs={'class': 'form-control'}),
            'end_date': DatePickerInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'new_technologies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Python, React, AWS, Improved app performance by 30%'}),
        }
        help_texts = {
            'new_technologies': 'List technologies and achievements, separated by commas or as free text.'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Optionally, you can parse and store new_technologies somewhere if needed
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class TechnicalSkillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['resume', 'technology', 'proficiency', 'years_experience', 'last_used', 'project_count', 'is_visible']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'technology': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'last_used': DatePickerInput(attrs={'class': 'form-control'}),
            'project_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['resume', 'degree', 'institution', 'location', 'start_date', 'end_date', 'gpa', 'description', 'is_visible']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': DatePickerInput(attrs={'class': 'form-control'}),
            'end_date': DatePickerInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 4, 'step': 0.1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        gpa = cleaned_data.get('gpa')
        
        # Validate dates
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")
        
        # Validate GPA
        if gpa is not None and (gpa < 0 or gpa > 4):
            raise forms.ValidationError("GPA must be between 0.0 and 4.0.")
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'category', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., fab fa-python'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['resume', 'title', 'role', 'start_date', 'end_date', 'description', 'technologies', 'outcomes', 'url', 'is_active']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': DatePickerInput(attrs={'class': 'form-control'}),
            'end_date': DatePickerInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'technologies': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'outcomes': JSONFieldWidget(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter project outcomes'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        
        # Handle outcomes field
        if 'outcomes' in form.cleaned_data:
            outcomes = form.cleaned_data['outcomes']
            if isinstance(outcomes, str):
                # Convert string to dict if needed
                try:
                    form.instance.outcomes = json.loads(outcomes)
                except json.JSONDecodeError:
                    # If JSON parsing fails, treat as plain text
                    form.instance.outcomes = {'description': outcomes}
            elif isinstance(outcomes, dict):
                form.instance.outcomes = outcomes
        
        return super().form_valid(form)

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['resume', 'name', 'issuer', 'issue_date', 'expiration_date', 'credential_id', 'verification_url', 'skills']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issuer': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': DatePickerInput(attrs={'class': 'form-control'}),
            'expiration_date': DatePickerInput(attrs={'class': 'form-control'}),
            'credential_id': forms.TextInput(attrs={'class': 'form-control'}),
            'verification_url': forms.URLInput(attrs={'class': 'form-control'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['resume', 'title', 'issuer', 'issue_date', 'category', 'description', 'impact_metrics', 'is_visible']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'issuer': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': DatePickerInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'impact_metrics': JSONFieldWidget(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter impact metrics'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        
        # Handle impact_metrics field
        if 'impact_metrics' in form.cleaned_data:
            impact_metrics = form.cleaned_data['impact_metrics']
            if isinstance(impact_metrics, str):
                # Convert string to dict if needed
                try:
                    form.instance.impact_metrics = json.loads(impact_metrics)
                except json.JSONDecodeError:
                    # If JSON parsing fails, treat as plain text
                    form.instance.impact_metrics = {'description': impact_metrics}
            elif isinstance(impact_metrics, dict):
                form.instance.impact_metrics = impact_metrics
        
        return super().form_valid(form)

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['resume', 'name', 'proficiency', 'certification', 'is_visible']
        widgets = {
            'resume': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'certification': forms.TextInput(attrs={'class': 'form-control'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_resumes = Resume.objects.filter(user=user)
            if user_resumes.exists():
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "Select a resume"
                self.fields['resume'].required = True
            else:
                self.fields['resume'].queryset = user_resumes
                self.fields['resume'].empty_label = "No resumes available - Create one first"
                self.fields['resume'].required = True
                self.fields['resume'].widget.attrs['disabled'] = 'disabled'

class ResumeTemplateSelectionForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['template']
        widgets = {
            'template': forms.Select(attrs={'class': 'form-select'}),
        }