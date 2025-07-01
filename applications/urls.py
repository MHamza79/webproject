from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.application_list, name='application_list'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('<int:pk>/edit/', views.ApplicationUpdateView.as_view(), name='application_update'),
    path('<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
] 