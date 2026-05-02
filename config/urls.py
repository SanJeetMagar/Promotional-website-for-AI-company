"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # path('v1/api/accounts/', include('src.apps.account.urls')),
    path('v1/api/team/', include('src.apps.team.urls')),
    path('v1/api/contact/', include('src.apps.contact.urls')), 
    path('v1/api/testimonials/', include('src.apps.testimonials.urls')),
    path('v1/api/logo/', include('src.apps.logo.urls')),
    path('v1/api/newsletter/', include('src.apps.newsletter.urls')),
    path('v1/api/services/', include('src.apps.services.urls')),
    path('v1/api/product/', include('src.apps.product.urls')),
    path('v1/api/faq/', include('src.apps.faq.urls')),
    # path('v1/api/portfolio/', include('src.apps.porfolio.urls')),
    # path('v1/api/inquiry/', include('src.apps.inquiry.urls')),
    # path('v1/api/career/', include('src.apps.career.urls')),
    # path('v1/api/blog/', include('src.apps.blog.urls')),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
