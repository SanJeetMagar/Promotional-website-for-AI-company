from rest_framework import serializers
from .models import BlogPost, Comment, BlogStatus


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'content','image', 'published_date']
        extra_kwargs = {
            'content': {'required': True,'allow_blank': False},
        }

class BlogPostListSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    def get_preview(self, obj):
        return obj.content[:150]

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'published_date', 'preview']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.filter(is_active=True), many=True).data
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