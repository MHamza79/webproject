from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job

def job_list(request):
    """Display all active job listings with optional search and filtering"""
    jobs = Job.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by experience level
    experience_level = request.GET.get('experience_level', '')
    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    context = {
        'jobs': jobs,
        'search_query': search_query,
        'job_type': job_type,
        'experience_level': experience_level,
        'location': location,
        'job_types': Job.JOB_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_LEVEL_CHOICES,
    }
    
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    """Display detailed information about a specific job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Get related jobs (same company or similar titles)
    related_jobs = Job.objects.filter(
        is_active=True
    ).exclude(id=job.id).filter(
        Q(company=job.company) | Q(title__icontains=job.title.split()[0])
    )[:3]
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    
    return render(request, 'jobs/job_detail.html', context)

@login_required
def job_create(request):
    """Allow authenticated users to create job listings"""
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        experience_level = request.POST.get('experience_level')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        benefits = request.POST.get('benefits')
        
        if title and company and location and description and requirements:
            job = Job.objects.create(
                title=title,
                company=company,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                salary_min=salary_min if salary_min else None,
                salary_max=salary_max if salary_max else None,
                description=description,
                requirements=requirements,
                benefits=benefits,
                posted_by=request.user
            )
            return redirect('job_detail', job_id=job.id)
    
    context = {
        'job_types': Job.JOB_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_LEVEL_CHOICES,
    }
    
    return render(request, 'jobs/job_form.html', context)
