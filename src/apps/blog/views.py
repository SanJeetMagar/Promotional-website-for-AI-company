from rest_framework import generics
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import BlogPost, Comment, BlogStatus
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@extend_schema(tags=['Blog'], summary="List published blog posts")
class BlogPostListView(APIView):
    def get(self, request):
        posts = BlogPost.objects.filter(status=BlogStatus.PUBLISHED).prefetch_related('tags')
        featured_posts = posts.filter(is_featured=True)[:5]
        latest_posts = posts.order_by('-published_date')[:10]      
        return Response(
        {
            'all_posts': BlogPostListSerializer(posts, many=True).data,
            'featured': BlogPostListSerializer(featured_posts, many=True).data,
            'latest': BlogPostListSerializer(latest_posts, many=True).data
        })

@extend_schema(tags=['Blog'], summary="Get blog post details")
class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer

    def get_object(self):   
        return get_object_or_404(
            BlogPost.objects.prefetch_related('comments', 'tags'),
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