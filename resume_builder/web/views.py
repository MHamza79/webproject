# Python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
from resume_builder.models import WorkExperience, Education, Project, Certification, Award, Language, Resume, TechnicalSkill
from resume_builder.forms import WorkExperienceForm, EducationForm, ProjectForm, CertificationForm, AwardForm, LanguageForm, TechnicalSkillForm, ResumeTemplateSelectionForm, ResumeForm

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

    def form_valid(self, form):
        # Ensure the resume belongs to the user
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

    def form_valid(self, form):
        resume = form.cleaned_data['resume']
        if resume.user != self.request.user:
            form.add_error('resume', 'You do not own this resume.')
            return self.form_invalid(form)
        return super().form_valid(form)

class AwardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = 'resume_builder/award/award_form.html'
    success_url = reverse_lazy('award_list')

    def test_func(self):
        return self.get_object().resume.user == self.request.user

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

    def form_valid(self, form):
        form.instance.user = self.request.user
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
        context['work_experiences'] = WorkExperience.objects.filter(resume=resume)
        context['educations'] = Education.objects.filter(resume=resume)
        context['projects'] = Project.objects.filter(resume=resume)
        context['certifications'] = Certification.objects.filter(resume=resume)
        context['awards'] = Award.objects.filter(resume=resume)
        context['languages'] = Language.objects.filter(resume=resume)
        context['technical_skills'] = TechnicalSkill.objects.filter(resume=resume)
        return context

class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume_builder/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def test_func(self):
        return self.get_object().user == self.request.user

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
        
        # Get all related data
        context = {
            'resume': resume,
            'work_experiences': WorkExperience.objects.filter(resume=resume),
            'educations': Education.objects.filter(resume=resume),
            'projects': Project.objects.filter(resume=resume),
            'certifications': Certification.objects.filter(resume=resume),
            'awards': Award.objects.filter(resume=resume),
            'languages': Language.objects.filter(resume=resume),
            'technical_skills': TechnicalSkill.objects.filter(resume=resume),
        }
        
        # Render HTML
        html_string = render_to_string(self.template_name, context)
        
        # Return HTML version for now (PDF generation can be added later)
        response = HttpResponse(html_string, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{resume.title.replace(" ", "_")}.html"'
        return response

class ResumeTemplateSelectionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    form_class = ResumeTemplateSelectionForm
    template_name = 'resume_builder/template_selection.html'
    success_url = reverse_lazy('resume_list')

    def test_func(self):
        return self.get_object().user == self.request.user