from src.apps.common.models import BaseModel
from django.db import models
class TeamMember(BaseModel):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='team_photos/')
    bio = models.TextField()
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CEOMessage(BaseModel):
    ceo_name = models.CharField(max_length=200)     
    ceo_title = models.CharField(max_length=200)    
    ceo_photo = models.ImageField(upload_to='ceo_photos/')
    quote = models.TextField()                       
    body_text = models.TextField()                   
    tagline = models.CharField(max_length=200)      
    sub_tagline = models.CharField(max_length=200)  
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "CEO Message"  