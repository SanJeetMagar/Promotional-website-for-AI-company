from .models import TeamMember, CEOMessage
from .serializers import TeamMemberSerializer, CEOMessageSerializer
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404


# --- TEAM MEMBER VIEWS ---

@extend_schema(tags=['Team Members'])
class TeamMemberListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer 
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)

@extend_schema(tags=['Team Members'])
class TeamMemberDetailView(generics.RetrieveAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['Team Members (Admin)'])
class AdminTeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['Team Members (Admin)'])
class TeamMemberCreateView(generics.CreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=['Team Members (Admin)'])
class TeamMemberUpdateView(generics.UpdateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=['Team Members (Admin)'])
class TeamMemberDeleteView(generics.DestroyAPIView):
    queryset = TeamMember.objects.all()
    permission_classes = [permissions.IsAdminUser]


# --- CEO MESSAGE VIEWS ---

@extend_schema(tags=['CEO Messages'])
class CEOMessageView(generics.RetrieveAPIView):
    """Public endpoint to grab the active CEO message for the frontend."""
    serializer_class = CEOMessageSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return get_object_or_404(CEOMessage, is_active=True)

@extend_schema(tags=['CEO Messages (Admin)'])
class AdminCEOMessageListView(generics.ListAPIView):
    queryset = CEOMessage.objects.all()
    serializer_class = CEOMessageSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['CEO Messages (Admin)'])
class CEOMessageDetailView(generics.RetrieveAPIView):
    queryset = CEOMessage.objects.all()
    serializer_class = CEOMessageSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['CEO Messages (Admin)'])
class CEOMessageCreateView(generics.CreateAPIView):
    queryset = CEOMessage.objects.all()
    serializer_class = CEOMessageSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=['CEO Messages (Admin)'])
class CEOMessageUpdateView(generics.UpdateAPIView):
    queryset = CEOMessage.objects.all()
    serializer_class = CEOMessageSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=['CEO Messages (Admin)'])
class CEOMessageDeleteView(generics.DestroyAPIView):
    queryset = CEOMessage.objects.all()
    permission_classes = [permissions.IsAdminUser]