from django.db import models
from src.apps.common.models import BaseModel

class Expertise(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='expertise_logos/')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name