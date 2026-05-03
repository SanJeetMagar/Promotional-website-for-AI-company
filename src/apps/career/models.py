from django.db import models
from src.apps.common.models import BaseModel

class Career(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()        