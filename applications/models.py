from django.db import models
from django.conf import settings
from jobs.models import Job

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.ForeignKey('resume_builder.Resume', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]
