from django.db import models
from src.apps.common.models import BaseModel

class BlogPost(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title