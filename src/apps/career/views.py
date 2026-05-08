from .models import CV, JobPosting
from .serializers import CVSerializer, JobPostingListSerializer, JobPostingDetailSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404

@extend_schema(description="List all career opportunities", tags=['JobsListing'])  
class JobPostingListView(generics.ListAPIView):
    queryset = JobPosting.objects.filter(status='published').prefetch_related('tags')
    serializer_class = JobPostingListSerializer 

@extend_schema(description="Get details of a specific job posting", tags=['JobDetails'])
class JobPostingDetailView(generics.RetrieveAPIView):
    queryset = JobPosting.objects.filter(status='published').prefetch_related('tags')
    serializer_class = JobPostingDetailSerializer
    lookup_field = 'slug'   

@extend_schema(description="Submit your CV for a job application", tags=['CVSubmission'])
class CVCreateView(generics.CreateAPIView):
    serializer_class = CVSerializer
    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        if slug:
            post = get_object_or_404(JobPosting, slug=slug, status='published')
            serializer.save(job=post)
        else:
            serializer.save()  # general CV, no job