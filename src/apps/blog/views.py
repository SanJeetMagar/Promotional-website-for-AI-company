from rest_framework import generics
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import BlogPost, Comment, BlogStatus
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, CommentSerializer


@extend_schema(tags=['Blog'], summary="List published blog posts")
class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer
    def get_queryset(self):
        return BlogPost.objects.filter(
            status=BlogStatus.PUBLISHED
        ).prefetch_related('comments')


@extend_schema(tags=['Blog'], summary="Get blog post details")
class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer

    def get_object(self):   
        return get_object_or_404(
            BlogPost.objects.prefetch_related('comments'),
            slug=self.kwargs['slug'],
            status=BlogStatus.PUBLISHED
    )
@extend_schema(tags=['Comment'], summary="Post a comment")
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(
            BlogPost,
            slug=self.kwargs['slug'],
            status=BlogStatus.PUBLISHED
        )
        serializer.save(blog_post=post)