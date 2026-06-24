from django.db import models
from src.apps.common.models import BaseModel
# Assuming Product is in the same file. If not, import it.

class Inquiry(BaseModel):
    class PriorityChoices(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class StatusChoices(models.TextChoices):
        NEW = 'NEW', 'New'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    
    # Optional link to a specific product they are asking about
    product = models.ForeignKey(
        'Product', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='inquiries'
    )
    
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    priority = models.CharField(
        max_length=10, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM
    )
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.NEW
    )

    class Meta:
        ordering = ['-created_at'] # Newest inquiries first
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.subject} - {self.name}"