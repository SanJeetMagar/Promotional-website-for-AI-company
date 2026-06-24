from rest_framework import generics, permissions
from .models import FAQ
from .serializers import FAQSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['FAQs'])
class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['FAQs'])
class FAQDetailView(generics.RetrieveAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['FAQs (Admin)'])
class FAQCreateView(generics.CreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['FAQs (Admin)'])
class FAQUpdateView(generics.UpdateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['FAQs (Admin)'])
class FAQDeleteView(generics.DestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]