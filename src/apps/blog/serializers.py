import math
from rest_framework import serializers
from .models import BlogPost, Comment, BlogStatus, KeyTakeaway, BlogImage, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class KeyTakeawaySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyTakeaway
        fields = ['id', 'content', 'order']


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'caption', 'image', 'order']


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'content', 'image', 'published_date', 'parent', 'replies']
        read_only_fields = ['published_date']
        extra_kwargs = {
            'content': {'required': True, 'allow_blank': False},
            'email': {'write_only': True},
        }

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_active=True), many=True).data
        return []


class BlogPostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'image', 'excerpt',
            'published_date', 'read_time', 'tags', 'is_featured',
            'view_count', 'comment_count'
        ]

    def get_comment_count(self, obj):
        return obj.comments.filter(is_active=True).count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    key_takeaways = KeyTakeawaySerializer(many=True, read_only=True)
    images = BlogImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    read_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'image', 'content',
            'excerpt', 'tags', 'published_date', 'comments',
            'key_takeaways', 'images', 'related_posts', 'read_time',
            'view_count', 'meta_description', 'meta_keywords'
        ]

    def get_comments(self, obj):
        # Only get top-level comments (no parent)
        top_level_comments = obj.comments.filter(is_active=True, parent__isnull=True)
        return CommentSerializer(top_level_comments, many=True).data

    def get_related_posts(self, obj):
        related_posts = BlogPost.objects.filter(
            tags__in=obj.tags.all(),
            status=BlogStatus.PUBLISHED
        ).exclude(id=obj.id).distinct()[:3]
        return BlogPostListSerializer(related_posts, many=True).data


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    key_takeaways = KeyTakeawaySerializer(many=True, required=False)
    images = BlogImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt',
            'image', 'status', 'is_featured', 'order', 'tags',
            'key_takeaways', 'images', 'meta_description', 'meta_keywords'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        key_takeaways_data = validated_data.pop('key_takeaways', [])
        tags_data = validated_data.pop('tags', [])
        
        blog_post = BlogPost.objects.create(**validated_data)
        
        if tags_data:
            blog_post.tags.set(tags_data)
        
        for takeaway_data in key_takeaways_data:
            KeyTakeaway.objects.create(blog_post=blog_post, **takeaway_data)
        
        return blog_post

    def update(self, instance, validated_data):
        key_takeaways_data = validated_data.pop('key_takeaways', None)
        tags_data = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        if key_takeaways_data is not None:
            # Remove old takeaways
            instance.key_takeaways.all().delete()
            # Create new ones
            for takeaway_data in key_takeaways_data:
                KeyTakeaway.objects.create(blog_post=instance, **takeaway_data)
        
        return instance
