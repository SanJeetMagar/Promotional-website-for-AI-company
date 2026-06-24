from django.urls import path    
from .views import (
    ExpertiseListView, AdminExpertiseListView, ExpertiseDetailView,
    ExpertiseCreateView, ExpertiseUpdateView, ExpertiseDeleteView
)

urlpatterns = [
    # Public
    path('', ExpertiseListView.as_view(), name='expertise-list'),
    path('<int:pk>/', ExpertiseDetailView.as_view(), name='expertise-detail'),
    
    # Admin
    path('admin/all/', AdminExpertiseListView.as_view(), name='admin-expertise-list'),
    path('admin/create/', ExpertiseCreateView.as_view(), name='expertise-create'),
    path('admin/<int:pk>/update/', ExpertiseUpdateView.as_view(), name='expertise-update'),
    path('admin/<int:pk>/delete/', ExpertiseDeleteView.as_view(), name='expertise-delete'),
]