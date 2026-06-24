from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import BlogPost, Comment, BlogStatus, Tag, BlogImage, KeyTakeaway
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer,
    CommentSerializer,
    TagSerializer,
    BlogImageSerializer
)
from .permissions import IsAdminOrReadOnly


# ============== Blog Post Views ==============

@extend_schema(
    tags=['Blog Posts'],
    summary="List and search blog posts",
    parameters=[
        OpenApiParameter('search', OpenApiTypes.STR, description='Search in title, content, and author'),
        OpenApiParameter('tag', OpenApiTypes.STR, description='Filter by tag slug'),
        OpenApiParameter('status', OpenApiTypes.STR, description='Filter by status (admin only)'),
        OpenApiParameter('featured', OpenApiTypes.BOOL, description='Filter featured posts'),
    ]
)
class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_date', 'view_count', 'title']
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = BlogPost.objects.select_related().prefetch_related(
            'tags',
            Prefetch('comments', queryset=Comment.objects.filter(is_active=True))
        )
        
        # Only show published posts to non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=BlogStatus.PUBLISHED)
        
        # Search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        # Filter by tag
        tag_slug = self.request.query_params.get('tag', None)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Filter by status (admin only)
        status_filter = self.request.query_params.get('status', None)
        if status_filter and self.request.user.is_staff:
            queryset = queryset.filter(status=status_filter)
        
        # Filter featured posts
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            is_featured = featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Get featured and latest posts for homepage
        if not request.query_params:
            featured_posts = queryset.filter(
                is_featured=True,
                status=BlogStatus.PUBLISHED
            )[:5]
            latest_posts = queryset.filter(
                is_featured=False,
                status=BlogStatus.PUBLISHED
            )[:10]
            
            return Response({
                'featured': self.get_serializer(featured_posts, many=True).data,
                'latest': self.get_serializer(latest_posts, many=True).data
            })
        
        # Default list behavior
        return super().list(request, *args, **kwargs)


@extend_schema(tags=['Blog Posts'], summary="Get blog post details")
class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = BlogPost.objects.select_related().prefetch_related(
            'comments__replies',
            'tags',
            'key_takeaways',
            'images'
        )
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=BlogStatus.PUBLISHED)
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=['Blog Posts'], summary="Create a new blog post")
class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Blog Posts'], summary="Update a blog post")
class BlogPostUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Blog Posts'], summary="Delete a blog post")
class BlogPostDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


@extend_schema(tags=['Blog Posts'], summary="Publish a draft blog post")
class BlogPostPublishView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug)
        blog_post.publish()
        serializer = BlogPostDetailSerializer(blog_post)
        return Response(serializer.data)


@extend_schema(tags=['Blog Posts'], summary="Archive a blog post")
class BlogPostArchiveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug)
        blog_post.archive()
        serializer = BlogPostDetailSerializer(blog_post)
        return Response(serializer.data)


# ============== Comment Views ==============

@extend_schema(tags=['Comments'], summary="List comments for a blog post")
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Comment.objects.filter(
            blog_post__slug=slug,
            is_active=True,
            parent__isnull=True  # Only top-level comments
        ).prefetch_related('replies')


@extend_schema(tags=['Comments'], summary="Create a comment on a blog post")
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        post = get_object_or_404(
            BlogPost,
            slug=slug,
            status=BlogStatus.PUBLISHED
        )
        serializer.save(blog_post=post)


@extend_schema(tags=['Comments'], summary="Update a comment")
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Comments'], summary="Delete a comment")
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ============== Tag Views ==============

@extend_schema(tags=['Tags'], summary="List all tags")
class TagListView(generics.ListAPIView):
    queryset = Tag.objects.annotate(
        post_count=Count('blog_posts', filter=Q(blog_posts__status=BlogStatus.PUBLISHED))
    )
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Tags'], summary="Create a new tag")
class TagCreateView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


@extend_schema(tags=['Tags'], summary="Update a tag")
class TagUpdateView(generics.UpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


@extend_schema(tags=['Tags'], summary="Delete a tag")
class TagDeleteView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


# ============== Blog Image Views ==============

@extend_schema(tags=['Blog Images'], summary="Upload images to a blog post")
class BlogImageCreateView(generics.CreateAPIView):
    queryset = BlogImage.objects.all()
    serializer_class = BlogImageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        blog_post = get_object_or_404(BlogPost, slug=slug)
        serializer.save(blog_post=blog_post)


@extend_schema(tags=['Blog Images'], summary="Delete a blog image")
class BlogImageDeleteView(generics.DestroyAPIView):
    queryset = BlogImage.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]