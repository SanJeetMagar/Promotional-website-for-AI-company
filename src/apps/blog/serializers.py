from rest_framework import serializers
from .models import BlogPost, Comment, BlogStatus


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
    related_posts = serializers.SerializerMethodField()

    def get_related_posts(self, obj):
        related_posts = BlogPost.objects.filter(
            tags__in=obj.tags.all(),
            status= BlogStatus.PUBLISHED
        ).exclude(id=obj.id).distinct()[:3]
        return BlogPostListSerializer(related_posts, many=True).data

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'content', 'published_date', 'comments', 'related_posts'    ]