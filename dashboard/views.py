from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta

@login_required(login_url='/accounts/login/')
def dashboard(request):
    # Sample data for demonstration
    profile_strength = 0  # Replace with actual calculation if available
    profile_strength_offset = 163.36 - (profile_strength * 1.6336)
    context = {
        'total_resumes': 3,
        'total_applications': 5,
        'total_jobs': 12,
        'profile_strength': profile_strength,
        'profile_strength_offset': profile_strength_offset,
        'recent_applications': [
            {
                'id': '#2457',
                'applicant': 'Hamza Ahmed',
                'job_title': 'Software Developer',
                'status': 'Approved',
                'date': '2024-01-15'
            },
            {
                'id': '#2147',
                'applicant': 'Abdullah Khan',
                'job_title': 'Data Analyst',
                'status': 'Pending',
                'date': '2024-01-14'
            },
            {
                'id': '#2049',
                'applicant': 'Umair Ali',
                'job_title': 'UI/UX Designer',
                'status': 'Approved',
                'date': '2024-01-13'
            }
        ],
        'recent_resumes': [
            {
                'name': 'Professional Resume',
                'owner': 'Hamza Ahmed',
                'last_updated': '2024-01-15'
            },
            {
                'name': 'Creative Portfolio',
                'owner': 'Abdullah Khan',
                'last_updated': '2024-01-14'
            }
        ],
        'recent_activities': [
            {
                'time': '32 min',
                'type': 'success',
                'content': 'Hamza Ahmed applied for Software Developer position'
            },
            {
                'time': '56 min',
                'type': 'danger',
                'content': 'Abdullah Khan updated his resume'
            },
            {
                'time': '2 hrs',
                'type': 'primary',
                'content': 'New job listing posted: Data Scientist'
            },
            {
                'time': '1 day',
                'type': 'info',
                'content': 'Umair Ali completed his profile'
            },
            {
                'time': '2 days',
                'type': 'warning',
                'content': 'System maintenance completed'
            }
        ]
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