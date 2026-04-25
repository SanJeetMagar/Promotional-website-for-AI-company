from django.db import models
from cloudinary.models import CloudinaryField
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='team_photos/')
    bio = models.TextField()

    def __str__(self):
        return self.name

class CEOMessage(models.Model):
    ceo_name = models.CharField(max_length=200)     
    ceo_title = models.CharField(max_length=200)    
    ceo_photo = CloudinaryField()
    quote = models.TextField()                       
    body_text = models.TextField()                   
    tagline = models.CharField(max_length=200)      
    sub_tagline = models.CharField(max_length=200)  
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "CEO Message"  