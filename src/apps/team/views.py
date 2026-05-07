from .models import TeamMember, CEOMessage
from .serializers import TeamMemberSerializer, CEOMessageSerializer
from rest_framework import generics     
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
@extend_schema(summary="Display team member",description="Get list of team members", tags=['Team Members'])
class TeamMemberListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer 
    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)
@extend_schema(summary="Active CEO Messages", description="Get list of active CEO messages", tags=['CEO Messages'])
class CEOMessageView(generics.RetrieveAPIView):
    serializer_class = CEOMessageSerializer

    def get_object(self):
        return get_object_or_404(CEOMessage, is_active=True)

