from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema 

@extend_schema(description="List all active blog posts", tags=['Blog'],summary="List of blog posts")
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_active=True)
    serializer_class = BlogPostSerializer   

@extend_schema(description="Post a new comment", tags=['Comment'],summary="Create a comment")
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer    
    