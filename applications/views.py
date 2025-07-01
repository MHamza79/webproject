from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import JobApplication
from jobs.models import Job
from resume_builder.models import Resume

@login_required
def application_list(request):
    """View for listing job applications"""
    applications = JobApplication.objects.filter(applicant=request.user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        applications = applications.filter(
            Q(job__title__icontains=search_query) |
            Q(job__company__icontains=search_query) |
            Q(cover_letter__icontains=search_query)
        )
    
    context = {
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'applications/application_list.html', context)

@login_required
def application_detail(request, pk):
    """View for displaying application details"""
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})

@login_required
def apply_for_job(request, job_id):
    """View for applying to a job"""
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    
    # Check if user already applied
    existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
    if existing_application:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('application_detail', pk=existing_application.pk)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        resume_id = request.POST.get('resume')
        
        # Get user's resumes
        user_resumes = Resume.objects.filter(user=request.user)
        
        application = JobApplication.objects.create(
            job=job,
            applicant=request.user,
            cover_letter=cover_letter,
            resume_id=resume_id if resume_id else None
        )
        
        messages.success(request, f'Successfully applied for {job.title} at {job.company}')
        return redirect('application_detail', pk=application.pk)
    
    # Get user's resumes for selection
    user_resumes = Resume.objects.filter(user=request.user)
    
    context = {
        'job': job,
        'user_resumes': user_resumes,
    }
    return render(request, 'applications/apply_for_job.html', context)

@login_required
def withdraw_application(request, pk):
    """View for withdrawing an application"""
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    
    if application.status in ['accepted', 'rejected']:
        messages.error(request, 'Cannot withdraw an application that has been accepted or rejected.')
        return redirect('application_detail', pk=application.pk)
    
    if request.method == 'POST':
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')
        return redirect('application_list')
    
    return render(request, 'applications/withdraw_application.html', {'application': application})

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobApplication
    fields = ['cover_letter', 'resume']
    template_name = 'applications/application_form.html'
    
    def test_func(self):
        application = self.get_object()
        return application.applicant == self.request.user and application.status == 'pending'
    
    def get_success_url(self):
        return reverse_lazy('application_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Application updated successfully.')
        return super().form_valid(form)
