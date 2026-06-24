from django.urls import path
from .views import (
    PublicGalleryListView,
    AdminCategoryListView,
    AdminCategoryDetailView,
    AdminBulkImageUploadView,
    AdminImageDetailView
)

urlpatterns = [
    # Public Endpoint
    path('', PublicGalleryListView.as_view(), name='public-gallery-list'),

    # Admin Category Endpoints
    path('admin/categories/', AdminCategoryListView.as_view(), name='admin-category-list-create'),
    path('admin/categories/<int:id>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),

    # Admin Image Endpoints
    path('admin/images/bulk-upload/', AdminBulkImageUploadView.as_view(), name='admin-image-bulk-upload'),
    path('admin/images/<int:id>/', AdminImageDetailView.as_view(), name='admin-image-detail'),
]