from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema 

@extend_schema(description="List all active blog posts", tags=['Blog'],summary="List of blog posts")
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_active=True)
    serializer_class = BlogPostSerializer   

    