from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(description="Get list of FAQs", tags=['FAQs'], summary="Display FAQs")
class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer    