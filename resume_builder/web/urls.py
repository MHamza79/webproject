# Python
from django.urls import path
from .views import (
    WorkExperienceListView, WorkExperienceCreateView, WorkExperienceUpdateView,
    WorkExperienceDeleteView, WorkExperienceDetailView,
    EducationListView, EducationCreateView, EducationUpdateView,
    EducationDeleteView, EducationDetailView,
    ProjectListView, ProjectCreateView, ProjectUpdateView,
    ProjectDeleteView, ProjectDetailView,
    CertificationListView, CertificationCreateView, CertificationUpdateView,
    CertificationDeleteView, CertificationDetailView,
    AwardListView, AwardCreateView, AwardUpdateView,
    AwardDeleteView, AwardDetailView,
    LanguageListView, LanguageCreateView, LanguageUpdateView,
    LanguageDeleteView, LanguageDetailView,
    TechnicalSkillListView, TechnicalSkillCreateView, TechnicalSkillUpdateView,
    TechnicalSkillDeleteView, TechnicalSkillDetailView,
    ResumeTemplateSelectionView,
    ResumeListView, ResumeCreateView, ResumeDetailView, ResumeUpdateView, 
    ResumeDeleteView, ResumeDownloadView
)

urlpatterns = [
    # Resume URLs
    path('resume/', ResumeListView.as_view(), name='resume_list'),
    path('resume/create/', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='resume_update'),
    path('resume/<int:pk>/delete/', ResumeDeleteView.as_view(), name='resume_delete'),
    path('resume/<int:pk>/download/', ResumeDownloadView.as_view(), name='resume_download'),
    path('resume/<int:pk>/select-template/', ResumeTemplateSelectionView.as_view(), name='resume_template_selection'),
    
    # Work Experience URLs
    path('work-experience/', WorkExperienceListView.as_view(), name='work_experience_list'),
    path('work-experience/add/', WorkExperienceCreateView.as_view(), name='work_experience_create'),
    path('work-experience/<int:pk>/edit/', WorkExperienceUpdateView.as_view(), name='work_experience_update'),
    path('work-experience/<int:pk>/delete/', WorkExperienceDeleteView.as_view(), name='work_experience_delete'),
    path('work-experience/<int:pk>/', WorkExperienceDetailView.as_view(), name='work_experience_detail'),
    
    # Education URLs
    path('education/', EducationListView.as_view(), name='education_list'),
    path('education/add/', EducationCreateView.as_view(), name='education_create'),
    path('education/<int:pk>/edit/', EducationUpdateView.as_view(), name='education_update'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education_detail'),
    
    # Project URLs
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    
    # Certification URLs
    path('certification/', CertificationListView.as_view(), name='certification_list'),
    path('certification/add/', CertificationCreateView.as_view(), name='certification_create'),
    path('certification/<int:pk>/edit/', CertificationUpdateView.as_view(), name='certification_update'),
    path('certification/<int:pk>/delete/', CertificationDeleteView.as_view(), name='certification_delete'),
    path('certification/<int:pk>/', CertificationDetailView.as_view(), name='certification_detail'),
    
    # Award URLs
    path('award/', AwardListView.as_view(), name='award_list'),
    path('award/add/', AwardCreateView.as_view(), name='award_create'),
    path('award/<int:pk>/edit/', AwardUpdateView.as_view(), name='award_update'),
    path('award/<int:pk>/delete/', AwardDeleteView.as_view(), name='award_delete'),
    path('award/<int:pk>/', AwardDetailView.as_view(), name='award_detail'),
    
    # Language URLs
    path('language/', LanguageListView.as_view(), name='language_list'),
    path('language/add/', LanguageCreateView.as_view(), name='language_create'),
    path('language/<int:pk>/edit/', LanguageUpdateView.as_view(), name='language_update'),
    path('language/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language_delete'),
    path('language/<int:pk>/', LanguageDetailView.as_view(), name='language_detail'),
    
    # Technical Skill URLs
    path('technicalskill/', TechnicalSkillListView.as_view(), name='technicalskill_list'),
    path('technicalskill/add/', TechnicalSkillCreateView.as_view(), name='technicalskill_create'),
    path('technicalskill/<int:pk>/edit/', TechnicalSkillUpdateView.as_view(), name='technicalskill_update'),
    path('technicalskill/<int:pk>/delete/', TechnicalSkillDeleteView.as_view(), name='technicalskill_delete'),
    path('technicalskill/<int:pk>/', TechnicalSkillDetailView.as_view(), name='technicalskill_detail'),
]