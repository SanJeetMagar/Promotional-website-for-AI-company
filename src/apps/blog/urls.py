from .views import BlogPostListView
from django.urls import path, include

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='blogpost-list'),
]