from django.db import models

class Expertise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='expertise_logos/')
    def __str__(self):
        return self.name