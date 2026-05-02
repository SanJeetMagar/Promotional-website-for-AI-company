from .models import Newsletter
from .serializers import NewsletterSerializer
from .tasks import send_welcome_email
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=NewsletterSerializer,
    responses=NewsletterSerializer,
    tags=["Newsletter"],
)
class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        """
        Override perform_create to trigger welcome email task
        after newsletter subscription is created.
        """
        instance = serializer.save()
        # Send welcome email asynchronously using Celery
        send_welcome_email.delay(instance.email) 
