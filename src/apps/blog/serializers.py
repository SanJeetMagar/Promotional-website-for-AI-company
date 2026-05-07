from rest_framework import serializers
from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'content','image', 'published_date']


class BlogPostListSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    def get_preview(self, obj):
        return obj.content[:150]

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'published_date', 'preview']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'content', 'published_date', 'comments']