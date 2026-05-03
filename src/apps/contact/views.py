from .models import ContactMessage, ContactInfo
from .serializers import ContactMessageSerializer, ContactInfoSerializer
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from .tasks import send_contact_email


class ContactAnonThrottle(AnonRateThrottle):
    """
    Limit anonymous users to 5 contact submissions per hour per IP address.
    """
    scope = 'contact_anon'


class ContactUserThrottle(UserRateThrottle):
    """
    Limit authenticated users to 20 contact submissions per hour.
    """
    scope = 'contact_user'


@extend_schema(description="Create a new contact message", tags=['Contact'])
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer 
    permission_classes = [AllowAny]
    throttle_classes = [ContactAnonThrottle, ContactUserThrottle]

    def perform_create(self, serializer):
        msg = serializer.save()
        try:
            send_contact_email.delay(msg.id)
        except Exception:
            # If Celery isn't available, attempt synchronous send as a best-effort fallback
            try:
                send_contact_email(msg.id)
            except Exception:
                pass

# @extend_schema(description="Retrieve contact information", tags=['Contact'])
# class ContactInfoView(generics.ListCreateAPIView):
