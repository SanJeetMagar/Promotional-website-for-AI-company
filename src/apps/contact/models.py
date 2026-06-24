from django.db import models
from src.apps.common.models import BaseModel

class ContactMessage(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    # REMOVED: created_at — BaseModel already provides it

    def __str__(self):
        return f"{self.first_name} - {self.subject}"

class ContactInfo(BaseModel):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    # REMOVED: created_at — BaseModel already provides it

    def __str__(self):
        return self.address

class SocialMediaLink(BaseModel):
    platform = models.CharField(max_length=255)
    url = models.URLField()
    # REMOVED: created_at — BaseModel already provides it

    def __str__(self):
        return self.platform