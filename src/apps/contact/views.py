from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema

@extend_schema(description="Create a new contact message", tags=['Contact'])
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer 
