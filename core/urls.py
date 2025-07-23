"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from allauth.account.views import LoginView

# Direct root URL to login for unauthenticated users, dashboard for authenticated

def root_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return LoginView.as_view()(request)

web_patterns = [
    path('admin/', admin.site.urls),
    # resume_builder web URLs
    path('web/', include('resume_builder.web.urls')),
    path('web/', include('accounts.web.urls')),
    path('accounts/', include('allauth.urls')),
    path('jobs/', include('jobs.urls')),
    path('applications/', include('applications.urls')),
    path('dashboard/', include('dashboard.urls')),  # Add dashboard URLs under 'dashboard/'
    path('', root_view, name='root'),
]
apis_patterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # resume_builder API URLs
    path('api/v1/', include('resume_builder.api.urls')),
    # accounts API URLs
    path('api/v1/', include('accounts.api.urls')),
]

urlpatterns = web_patterns + apis_patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)