# Python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
import os
import re

from resume_builder.models import WorkExperience, Education, Project, Certification, Award, Language, Resume, TechnicalSkill, ResumeTemplate
from resume_builder.forms import WorkExperienceForm, EducationForm, ProjectForm, CertificationForm, AwardForm, LanguageForm, TechnicalSkillForm, ResumeTemplateSelectionForm, ResumeForm
from resume_builder.utils import generate_resume_pdf, get_safe_filename
from resume_builder.services import ResumeAnalyzer, ResumeEnhancer

class WorkExperienceListView(LoginRequiredMixin, ListView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_list.html'
    context_object_name = 'experiences'

    def get_queryset(self):
        return WorkExperience.objects.filter(resume__user=self.request.user)

class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'resume_builder/work_experience/work_experience_form.html'
    success_url = reverse_lazy('work_experience_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        user_resumes = Resume.objects.filter(user=user)
        if not user_resumes.exists():
            # Create a default resume for the user with a unique slug
            from django.utils.text import slugify
            base_slug = slugify(f"{user.username}-my-first-resume")
            slug = base_slug
            counter = 1
            while Resume.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            default_resume = Resume.objects.create(
                user=user,
                title='My First Resume',
                slug=slug,
                summary='',
                tags=[],
                template=ResumeTemplate.objects.first().name if ResumeTemplate.objects.first() else 'modern',
                visibility='PRIVATE',
            )
            user_resumes = Resume.objects.filter(user=user)
        kwargs['user'] = user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        user_resumes = Resume.objects.filter(user=user)
        if user_resumes.exists():
            initial['resume'] = user_resumes.first()
        return initial

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class WorkExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'resume_builder/work_experience/work_experience_form.html'
    success_url = reverse_lazy('work_experience_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Remove 'user' kwarg, not needed anymore
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class WorkExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_confirm_delete.html'
    success_url = reverse_lazy('work_experience_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class WorkExperienceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkExperience
    template_name = 'resume_builder/work_experience/work_experience_detail.html'
    context_object_name = 'experience'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'resume_builder/education/education_list.html'
    context_object_name = 'educations'

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume_builder/education/education_form.html'
    success_url = reverse_lazy('education_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume_builder/education/education_form.html'
    success_url = reverse_lazy('education_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'resume_builder/education/education_confirm_delete.html'
    success_url = reverse_lazy('education_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class EducationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Education
    template_name = 'resume_builder/education/education_detail.html'
    context_object_name = 'education'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'resume_builder/project/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(resume__user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume_builder/project/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume_builder/project/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'resume_builder/project/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'resume_builder/project/project_detail.html'
    context_object_name = 'project'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class CertificationListView(LoginRequiredMixin, ListView):
    model = Certification
    template_name = 'resume_builder/certification/certification_list.html'
    context_object_name = 'certifications'

    def get_queryset(self):
        return Certification.objects.filter(resume__user=self.request.user)

class CertificationCreateView(LoginRequiredMixin, CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'resume_builder/certification/certification_form.html'
    success_url = reverse_lazy('certification_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class CertificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'resume_builder/certification/certification_form.html'
    success_url = reverse_lazy('certification_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class CertificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certification
    template_name = 'resume_builder/certification/certification_confirm_delete.html'
    success_url = reverse_lazy('certification_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class CertificationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Certification
    template_name = 'resume_builder/certification/certification_detail.html'
    context_object_name = 'certification'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class AwardListView(LoginRequiredMixin, ListView):
    model = Award
    template_name = 'resume_builder/award/award_list.html'
    context_object_name = 'awards'

    def get_queryset(self):
        return Award.objects.filter(resume__user=self.request.user)

class AwardCreateView(LoginRequiredMixin, CreateView):
    model = Award
    form_class = AwardForm
    template_name = 'resume_builder/award/award_form.html'
    success_url = reverse_lazy('award_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        # Patch: Always set impact_metrics to {} if not provided
        if not form.instance.impact_metrics:
            form.instance.impact_metrics = {}
        return super().form_valid(form)

class AwardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = 'resume_builder/award/award_form.html'
    success_url = reverse_lazy('award_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

    def form_valid(self, form):
        # Patch: Always set impact_metrics to {} if not provided
        if not form.instance.impact_metrics:
            form.instance.impact_metrics = {}
        return super().form_valid(form)

class AwardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Award
    template_name = 'resume_builder/award/award_confirm_delete.html'
    success_url = reverse_lazy('award_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class AwardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Award
    template_name = 'resume_builder/award/award_detail.html'
    context_object_name = 'award'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class LanguageListView(LoginRequiredMixin, ListView):
    model = Language
    template_name = 'resume_builder/language/language_list.html'
    context_object_name = 'languages'

    def get_queryset(self):
        return Language.objects.filter(resume__user=self.request.user)

class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'resume_builder/language/language_form.html'
    success_url = reverse_lazy('language_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class LanguageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'resume_builder/language/language_form.html'
    success_url = reverse_lazy('language_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class LanguageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Language
    template_name = 'resume_builder/language/language_confirm_delete.html'
    success_url = reverse_lazy('language_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class LanguageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Language
    template_name = 'resume_builder/language/language_detail.html'
    context_object_name = 'language'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class TechnicalSkillListView(LoginRequiredMixin, ListView):
    model = TechnicalSkill
    template_name = 'resume_builder/technicalskill/technicalskill_list.html'
    context_object_name = 'technicalskills'

    def get_queryset(self):
        return TechnicalSkill.objects.filter(resume__user=self.request.user)

class TechnicalSkillCreateView(LoginRequiredMixin, CreateView):
    model = TechnicalSkill
    form_class = TechnicalSkillForm
    template_name = 'resume_builder/technicalskill/technicalskill_form.html'
    success_url = reverse_lazy('technicalskill_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class TechnicalSkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TechnicalSkill
    form_class = TechnicalSkillForm
    template_name = 'resume_builder/technicalskill/technicalskill_form.html'
    success_url = reverse_lazy('technicalskill_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class TechnicalSkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TechnicalSkill
    template_name = 'resume_builder/technicalskill/technicalskill_confirm_delete.html'
    success_url = reverse_lazy('technicalskill_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class TechnicalSkillDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TechnicalSkill
    template_name = 'resume_builder/technicalskill/technicalskill_detail.html'
    context_object_name = 'technicalskill'

    def test_func(self):
        return self.get_object().resume.user == self.request.user

# Resume Views
class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume_builder/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Handle tags field - convert comma-separated string to list
        if 'tags' in form.cleaned_data and form.cleaned_data['tags']:
            tags_text = form.cleaned_data['tags']
            if isinstance(tags_text, str):
                # Convert comma-separated string to list
                tags_list = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
                form.instance.tags = tags_list
        return super().form_valid(form)

class ResumeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resume
    template_name = 'resume_builder/resume_detail.html'
    context_object_name = 'resume'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        context['work_experiences'] = resume.work_experiences.all()
        context['educations'] = resume.educations.all()
        context['projects'] = resume.projects.all()
        context['certifications'] = resume.certifications.all()
        context['awards'] = resume.awards.all()
        context['languages'] = resume.languages.all()
        context['technical_skills'] = resume.technical_skills.all()
        return context

class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        # Handle tags field - convert comma-separated string to list
        if 'tags' in form.cleaned_data and form.cleaned_data['tags']:
            tags_text = form.cleaned_data['tags']
            if isinstance(tags_text, str):
                # Convert comma-separated string to list
                tags_list = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
                form.instance.tags = tags_list
        return super().form_valid(form)

class ResumeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resume
    template_name = 'resume_builder/resume_confirm_delete.html'
    success_url = reverse_lazy('resume_list')

    def test_func(self):
        return self.get_object().user == self.request.user

class ResumeDownloadView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resume
    template_name = 'resume_builder/resume_pdf.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get(self, request, *args, **kwargs):
        resume = self.get_object()
        
        try:
            # Generate PDF using utility function
            pdf_content = generate_resume_pdf(resume)
            
            # Create safe filename
            safe_filename = get_safe_filename(resume.title)
            
            # Create response with PDF content
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}.pdf"'
            return response
            
        except Exception as e:
            # Log the error and return a user-friendly message
            messages.error(request, f"Error generating PDF: {str(e)}")
            return redirect('resume_detail', pk=resume.pk)

class ResumeTemplateSelectionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    form_class = ResumeTemplateSelectionForm
    template_name = 'resume_builder/template_selection.html'
    success_url = reverse_lazy('resume_list')

    def test_func(self):
        return self.get_object().user == self.request.user

class ResumeAnalysisView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """AI-powered resume analysis and improvement suggestions"""
    model = Resume
    template_name = 'resume_builder/resume_analysis.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        
        # Initialize analyzer
        analyzer = ResumeAnalyzer(resume)
        enhancer = ResumeEnhancer()
        
        # Get analysis results
        context['ats_score'] = analyzer.analyze_ats_score()
        context['suggestions'] = analyzer.get_improvement_suggestions()
        context['improvement_suggestions'] = analyzer.get_improvement_suggestions()
        context['completion_percentage'] = resume.get_completion_percentage()
        context['ats_analysis'] = enhancer.optimize_for_ats(resume)
        
        # Get keyword suggestions
        context['keywords'] = analyzer.suggest_keywords()
        context['keyword_suggestions'] = analyzer.suggest_keywords()
        
        # Get action verb suggestions
        context['action_verbs'] = analyzer.ACTION_VERBS[:10]
        
        # Resume statistics
        context['stats'] = {
            'total_words': len(analyzer.content.split()),
            'action_verbs_used': sum(1 for verb in analyzer.ACTION_VERBS if verb in analyzer.content),
            'numbers_used': len(re.findall(r'\d+', analyzer.content)),
            'sections_completed': sum([
                bool(resume.summary),
                resume.work_experiences.exists(),
                resume.educations.exists(),
                resume.technical_skills.exists(),
                resume.projects.exists(),
                resume.certifications.exists(),
                resume.awards.exists(),
                resume.languages.exists(),
            ])
        }
        
        # Calculate progress offset for circular progress bar
        # Formula: (100 - ats_score) * 3.14 to create the offset
        context['progress_offset'] = (100 - context['ats_score']) * 3.14
        
        return context

class CoverLetterGeneratorView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Generate cover letters based on resume"""
    model = Resume
    template_name = 'resume_builder/cover_letter_generator.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        analyzer = ResumeAnalyzer(resume)
        
        # Get job details from request
        job_title = self.request.GET.get('job_title', 'Software Engineer')
        company = self.request.GET.get('company', 'Tech Company')
        
        # Generate cover letter
        context['cover_letter'] = analyzer.generate_cover_letter_content(job_title, company)
        context['job_title'] = job_title
        context['company'] = company
        
        return context

class ResumeVariationsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Generate different resume variations for different job applications"""
    model = Resume
    template_name = 'resume_builder/resume_variations.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        enhancer = ResumeEnhancer()
        
        # Get job title from request
        job_title = self.request.GET.get('job_title', 'Software Engineer')
        
        # Generate variations
        context['variations'] = enhancer.generate_resume_variations(resume, job_title)
        context['job_title'] = job_title
        
        return context

class BulletPointGeneratorView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Generate AI-powered bullet point suggestions"""
    model = Resume
    template_name = 'resume_builder/bullet_point_generator.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        analyzer = ResumeAnalyzer(resume)
        
        # Get job details from request
        job_title = self.request.GET.get('job_title', 'Software Engineer')
        company = self.request.GET.get('company', 'Tech Company')
        
        # Generate bullet point suggestions
        context['bullet_suggestions'] = analyzer.suggest_bullet_points(job_title, company)
        context['job_title'] = job_title
        context['company'] = company
        
        return context