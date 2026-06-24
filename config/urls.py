from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static

# Import the new Analytics View
from src.apps.common.views import AdminDashboardAnalyticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    # === NEW ANALYTICS ENDPOINT ===
    path('v1/api/admin/analytics/', AdminDashboardAnalyticsView.as_view(), name='admin-analytics'),
    
    # Existing Apps
    path('v1/api/accounts/', include('src.apps.accounts.urls')),
    path('v1/api/team/', include('src.apps.team.urls')),
    path('v1/api/contact/', include('src.apps.contact.urls')), 
    path('v1/api/testimonials/', include('src.apps.testimonials.urls')),
    path('v1/api/logo/', include('src.apps.logo.urls')),
    path('v1/api/newsletter/', include('src.apps.newsletter.urls')),
    path('v1/api/services/', include('src.apps.services.urls')),
    path('v1/api/product/', include('src.apps.product.urls')),
    path('v1/api/faq/', include('src.apps.faq.urls')),
    path('v1/api/career/', include('src.apps.career.urls')),
    path('v1/api/blog/', include('src.apps.blog.urls')),    
    path('v1/api/inquiry/', include('src.apps.inquiry.urls')),
    path('v1/api/events/', include('src.apps.events.urls')),
    path('v1/api/gallery/', include('src.apps.gallery.urls')),
    
    # path('v1/api/portfolio/', include('src.apps.portfolio.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)