from .views import BlogPostDetailView, BlogPostListView, CommentCreateView
from django.urls import path, include

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blogpost-list'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blogpost-detail'),
    path('<slug:slug>/comments/', CommentCreateView.as_view(), name='comment-create'),
]