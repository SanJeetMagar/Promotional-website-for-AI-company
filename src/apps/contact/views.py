from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny


@extend_schema(description="Create a new contact message", tags=['Contact'])
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer 
    permission_classes = [AllowAny]