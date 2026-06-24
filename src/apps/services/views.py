from .models import Expertise
from .serializers import ExpertiseSerializer
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Services"])
class ExpertiseListView(generics.ListAPIView):
    """Public Endpoint: Only shows active services"""
    serializer_class = ExpertiseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Expertise.objects.filter(is_active=True)

@extend_schema(tags=["Services"])
class ExpertiseDetailView(generics.RetrieveAPIView):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=["Services (Admin)"])
class AdminExpertiseListView(generics.ListAPIView):
    """Admin Endpoint: Shows all services including inactive ones"""
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=["Services (Admin)"])
class ExpertiseCreateView(generics.CreateAPIView):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=["Services (Admin)"])
class ExpertiseUpdateView(generics.UpdateAPIView):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=["Services (Admin)"])
class ExpertiseDeleteView(generics.DestroyAPIView):
    queryset = Expertise.objects.all()
    permission_classes = [permissions.IsAdminUser]