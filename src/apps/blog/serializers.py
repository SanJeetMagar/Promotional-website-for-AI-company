from .models import BlogPost, Comment
from rest_framework import serializers  

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'content', 'published_date', 'is_active', 'order', 'comments']
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'name', 'email', 'content', 'published_date', 'is_active']