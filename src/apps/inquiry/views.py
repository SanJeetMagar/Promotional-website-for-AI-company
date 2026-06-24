from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Inquiry
from .serializers import PublicInquiryCreateSerializer, AdminInquirySerializer


@extend_schema_view(
    post=extend_schema(
        summary="Submit an Inquiry",
        description="Public endpoint for users to submit an inquiry from the website. No authentication required.",
        tags=["Inquiry (Public)"],
    )
)
class InquirySubmitView(generics.CreateAPIView):
    """Public endpoint: Anyone can create an inquiry"""
    queryset = Inquiry.objects.all()
    serializer_class = PublicInquiryCreateSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="List all Inquiries (Admin)",
        description="Admin frontend endpoint to list and filter inquiries by status and priority.",
        tags=["Inquiry (Admin)"],
    )
)
class AdminInquiryListView(generics.ListAPIView):
    """Admin endpoint: List all inquiries with filtering and searching"""
    queryset = Inquiry.objects.all()
    serializer_class = AdminInquirySerializer
    permission_classes = [permissions.IsAdminUser] # Only staff/admin users
    
    # Allows filtering from the frontend, e.g.: /inquiries/?status=NEW&priority=HIGH
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'product']
    search_fields = ['name', 'email', 'subject', 'company_name']
    ordering_fields = ['created_at', 'priority']


@extend_schema_view(
    get=extend_schema(
        summary="Get Inquiry Detail (Admin)",
        tags=["Inquiry (Admin)"],
    ),
    put=extend_schema(
        summary="Update Inquiry (Admin)",
        description="Update an inquiry (e.g., changing status to RESOLVED).",
        tags=["Inquiry (Admin)"],
    ),
    patch=extend_schema(
        summary="Partial Update Inquiry (Admin)",
        tags=["Inquiry (Admin)"],
    ),
    delete=extend_schema(
        summary="Delete Inquiry (Admin)",
        tags=["Inquiry (Admin)"],
    )
)
class AdminInquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint: View, Update, or Delete a specific inquiry"""
    queryset = Inquiry.objects.all()
    serializer_class = AdminInquirySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'