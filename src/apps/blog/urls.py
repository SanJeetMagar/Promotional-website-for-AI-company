from django.urls import path
from .views import (
    BlogPostListView, BlogPostDetailView, BlogPostCreateView,
    BlogPostUpdateView, BlogPostDeleteView, BlogPostPublishView,
    BlogPostArchiveView, CommentListView, CommentCreateView,
    CommentUpdateView, CommentDeleteView, TagListView, TagCreateView,
    TagUpdateView, TagDeleteView, BlogImageCreateView, BlogImageDeleteView,
)

app_name = 'blog'

urlpatterns = [
    # Blog Post URLs
    path('posts/', BlogPostListView.as_view(), name='post-list'),
    path('posts/create/', BlogPostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='post-update'),
    path('posts/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post-delete'),
    path('posts/<slug:slug>/publish/', BlogPostPublishView.as_view(), name='post-publish'),
    path('posts/<slug:slug>/archive/', BlogPostArchiveView.as_view(), name='post-archive'),

    # Comment URLs
    path('posts/<slug:slug>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<slug:slug>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Tag URLs
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('tags/<slug:slug>/update/', TagUpdateView.as_view(), name='tag-update'),
    path('tags/<slug:slug>/delete/', TagDeleteView.as_view(), name='tag-delete'),

    # Image URLs
    path('posts/<slug:slug>/images/upload/', BlogImageCreateView.as_view(), name='image-upload'),
    path('images/<int:pk>/delete/', BlogImageDeleteView.as_view(), name='image-delete'),
]