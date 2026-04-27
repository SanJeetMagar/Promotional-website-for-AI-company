from .models import Newsletter
from .serializers import NewsletterSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=NewsletterSerializer,
    responses=NewsletterSerializer,
    tags=["Newsletter"],
)
class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer 
