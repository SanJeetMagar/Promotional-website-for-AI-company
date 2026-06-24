from django.db import models

# Create your models here.
from django.db import models
from src.apps.common.models import BaseModel
from src.apps.common.slug import generate_unique_slug

class GalleryCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Gallery Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(GalleryCategory, self.name)
        super().save(*args, **kwargs)


class GalleryImage(BaseModel):
    category = models.ForeignKey(
        GalleryCategory, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Image in {self.category.name}"