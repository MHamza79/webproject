from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta

@login_required(login_url='/accounts/login/')
def dashboard(request):
    from resume_builder.models import Resume
    from applications.models import JobApplication
    user = request.user
    # Query user resumes
    user_resumes = Resume.objects.filter(user=user)
    total_resumes = user_resumes.count()
    # Query applications
    total_applications = JobApplication.objects.filter(applicant=user).count()
    # Section checklist (example, adjust as needed)
    resume_sections = [
        {'name': 'Personal Info', 'completed': bool(user.first_name and user.last_name), 'add_url': '#'},
        {'name': 'Work Experience', 'completed': user_resumes.filter(work_experiences__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Education', 'completed': user_resumes.filter(educations__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Projects', 'completed': user_resumes.filter(projects__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Certifications', 'completed': user_resumes.filter(certifications__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Awards', 'completed': user_resumes.filter(awards__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Languages', 'completed': user_resumes.filter(languages__isnull=False).exists(), 'add_url': '#'},
        {'name': 'Technical Skills', 'completed': user_resumes.filter(technical_skills__isnull=False).exists(), 'add_url': '#'},
    ]
    total_sections = len(resume_sections)
    sections_completed = sum(1 for s in resume_sections if s['completed'])
    section_completion_percent = int((sections_completed / total_sections) * 100) if total_sections else 0
    # Profile strength (simple example)
    profile_strength = section_completion_percent
    profile_strength_offset = 163.36 - (profile_strength * 1.6336)
    # Recent activities (dummy for now)
    recent_activities = [
        {'time': 'Just now', 'type': 'success', 'content': 'Welcome to your dashboard!'},
    ]
    context = {
        'total_resumes': total_resumes,
        'total_applications': total_applications,
        'profile_strength': profile_strength,
        'profile_strength_offset': profile_strength_offset,
        'section_completion_percent': section_completion_percent,
        'sections_completed': sections_completed,
        'total_sections': total_sections,
        'user_resumes': user_resumes,
        'resume_sections': resume_sections,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard/dashboard.html', context)

def settings_view(request):
    """Settings page for user preferences"""
    context = {
        'user': request.user,
        'settings_sections': [
            {
                'title': 'Profile Settings',
                'icon': 'bi-person',
                'description': 'Update your personal information and profile details'
            },
            {
                'title': 'Notification Settings',
                'icon': 'bi-bell',
                'description': 'Configure email and push notifications'
            },
            {
                'title': 'Privacy Settings',
                'icon': 'bi-shield-lock',
                'description': 'Manage your privacy and data preferences'
            },
            {
                'title': 'Account Security',
                'icon': 'bi-key',
                'description': 'Change password and security settings'
            }
        ]
    }
    return render(request, 'dashboard/settings.html', context)