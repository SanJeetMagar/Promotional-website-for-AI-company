from .models import ContactMessage, ContactInfo
from .serializers import ContactMessageSerializer, ContactInfoSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny


@extend_schema(description="Create a new contact message", tags=['Contact'])
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer 
    permission_classes = [AllowAny]

@extend_schema(description="Retrieve contact information", tags=['Contact'])
class ContactInfoView(generics.RetrieveAPIView):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    def get_object(self):
        return self.queryset.first()  # Assuming there's only one contact info entry
    permission_classes = [AllowAny]