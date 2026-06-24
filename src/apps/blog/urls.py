from django.urls import path
from .views import (
    # Blog Post Views
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    BlogPostPublishView,
    BlogPostArchiveView,
    # Comment Views
    CommentListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    # Tag Views
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    # Image Views
    BlogImageCreateView,
    BlogImageDeleteView,
)

app_name = 'blog'

urlpatterns = [
    # Blog Post URLs
    path('posts/', BlogPostListView.as_view(), name='post-list'),
    path('posts/create/', BlogPostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/update/', BlogPostUpdateView.as_view(), name='post-update'),
    path('posts/delete/', BlogPostDeleteView.as_view(), name='post-delete'),
    path('posts/publish/', BlogPostPublishView.as_view(), name='post-publish'),
    path('posts/archive/', BlogPostArchiveView.as_view(), name='post-archive'),
    
    # Comment URLs
    path('posts/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # Tag URLs
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('tags/update/', TagUpdateView.as_view(), name='tag-update'),
    path('tags/delete/', TagDeleteView.as_view(), name='tag-delete'),
    
    # Image URLs
    path('posts/images/upload/', BlogImageCreateView.as_view(), name='image-upload'),
    path('images/delete/', BlogImageDeleteView.as_view(), name='image-delete'),
]