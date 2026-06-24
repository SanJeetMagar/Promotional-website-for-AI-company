from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from src.apps.common.slug import generate_unique_slug
from src.apps.common.models import BaseModel

User = get_user_model()


class BlogStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Tag, self.name)
        super().save(*args, **kwargs)


class BlogPost(BaseModel):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    author = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description for preview")
    published_date = models.DateTimeField(null=True, blank=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    view_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT,
        db_index=True
    )
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-published_date', 'order']
        indexes = [
            models.Index(fields=['-published_date', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(BlogPost, self.title)
        
        # Auto-set excerpt from content if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...'
        
        # Auto-set published_date when status changes to published
        if self.status == BlogStatus.PUBLISHED and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)

    def publish(self):
        """Publish the blog post"""
        self.status = BlogStatus.PUBLISHED
        if not self.published_date:
            self.published_date = timezone.now()
        self.save()

    def archive(self):
        """Archive the blog post"""
        self.status = BlogStatus.ARCHIVED
        self.save()

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def read_time(self):
        """Calculate estimated read time"""
        import math
        words = len(self.content.split())
        return math.ceil(words / 200)


class Comment(BaseModel):
    blog_post = models.ForeignKey(
        BlogPost,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f'Comment by {self.name} on {self.blog_post.title}'


class BlogImage(BaseModel):
    blog_post = models.ForeignKey(
        BlogPost,
        related_name='images',
        on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='blog_images/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'Image for {self.blog_post.title}'


class KeyTakeaway(BaseModel):
    blog_post = models.ForeignKey(
        BlogPost,
        related_name='key_takeaways',
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Takeaway: {self.content[:50]}'
