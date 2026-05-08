from .views import JobPostingListView, JobPostingDetailView, CVCreateView
from django.urls import path

urlpatterns = [
    path('jobs/', JobPostingListView.as_view(), name='job-list'),
    path('jobs/<slug:slug>/', JobPostingDetailView.as_view(), name='job-detail'),
    path('cv/', CVCreateView.as_view(), name='cv-create'),
]