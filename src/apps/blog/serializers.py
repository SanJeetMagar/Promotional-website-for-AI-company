import math
from rest_framework import serializers
from .models import BlogPost, Comment, BlogStatus, KeyTakeaway, BlogImage, Tag
class KeyTakeawaySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyTakeaway
        fields = ['id', 'content']

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'caption', 'image', 'order']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'content','image', 'published_date']
        extra_kwargs = {
            'content': {'required': True,'allow_blank': False},
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BlogPostListSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    def get_preview(self, obj):
        return obj.content[:150]
    read_time = serializers.SerializerMethodField()
    def get_read_time(self, obj):
        words = len(obj.content.split())
        return math.ceil(words / 200)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'published_date', 'read_time','preview', 'tags']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.filter(is_active=True), many=True, context=self.context).data

    related_posts = serializers.SerializerMethodField()

    def get_related_posts(self, obj):
        related_posts = BlogPost.objects.filter(
            tags__in=obj.tags.all(),
            status= BlogStatus.PUBLISHED
        ).exclude(id=obj.id).distinct()[:3]
        return BlogPostListSerializer(related_posts, many=True, context={'request': self.context.get('request')}).data
    key_takeaways = KeyTakeawaySerializer(many=True, read_only=True)
    images = BlogImageSerializer(many=True, read_only=True)
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'image', 'content', 'published_date', 'comments','key_takeaways', 'images', 'related_posts'    ]