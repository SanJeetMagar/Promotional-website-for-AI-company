from django.urls import path
from .views import (
    InquirySubmitView,
    AdminInquiryListView,
    AdminInquiryDetailView
)

urlpatterns = [
    # ... your product urls ...
    
    # Public route
    path('inquiries/submit/', InquirySubmitView.as_view(), name='inquiry-submit'),
    
    # Admin routes (for your custom frontend admin panel)
    path('admin-panel/inquiries/', AdminInquiryListView.as_view(), name='admin-inquiry-list'),
    path('admin-panel/inquiries/<int:id>/', AdminInquiryDetailView.as_view(), name='admin-inquiry-detail'),
]