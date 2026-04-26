from django.db import models

class Logo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='logos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name