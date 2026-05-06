from .models import TeamMember, CEOMessage
from .serializers import TeamMemberSerializer, CEOMessageSerializer
from rest_framework import generics     
from drf_spectacular.utils import extend_schema

@extend_schema(summary="Display team member",description="Get list of team members", tags=['Team Members'])
class TeamMemberListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer 
    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)
@extend_schema(summary="Active CEO Messages", description="Get list of active CEO messages", tags=['CEO Messages'])
class CEOMessageListView(generics.ListAPIView):
    def get_queryset(self):
        return CEOMessage.objects.filter(is_active=True)
    serializer_class = CEOMessageSerializer     


