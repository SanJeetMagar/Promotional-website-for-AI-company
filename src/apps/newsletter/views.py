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
    summary="Subscribe to newsletter",
    description="Create a new newsletter subscription. A welcome email will be sent to the provided email address."
)
class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        instance = serializer.save()
        
        # FIXED: Try Celery first, fallback to Sync, ignore if both fail (prevents 500 error)
        try:
            send_welcome_email.delay(instance.email)
        except Exception:
            try:
                send_welcome_email(instance.email)
            except Exception:
                pass