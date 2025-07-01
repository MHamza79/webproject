from django.urls import *
from dashboard.views import dashboard, settings_view


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', settings_view, name='settings'),
]