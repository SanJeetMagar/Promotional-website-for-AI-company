from django.db import models
from django.utils import timezone
from src.apps.common.slug import generate_unique_slug
from src.apps.common.models import BaseModel


class BlogStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'

class BlogPost(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT
    )

    class Meta:
        ordering = ['order', 'published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(BlogPost, self.title)
        # Auto-set published_date when status changes to published
        if self.status == BlogStatus.PUBLISHED and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def publish(self):
        self.status = BlogStatus.PUBLISHED
        if not self.published_date:  # Don't overwrite original publish date
            self.published_date = timezone.now()
        self.save()

    def archive(self):
        self.status = BlogStatus.ARCHIVED
        self.save()


class Comment(BaseModel):
    blog_post = models.ForeignKey(
        BlogPost,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on post {self.blog_post_id}'