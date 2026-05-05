from .views import BlogPostListView, CommentCreateView
from django.urls import path, include

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='blogpost-list'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
]