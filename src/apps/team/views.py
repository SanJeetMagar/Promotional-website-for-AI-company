from .models import TeamMember, CEOMessage
from .serializers import TeamMemberSerializer, CEOMessageSerializer
from rest_framework import generics     
from drf_spectacular.utils import extend_schema

@extend_schema(description="Get list of team members", tags=['Team Members'])
class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer 

@extend_schema(description="Get list of active CEO messages", tags=['CEO Messages'])
class CEOMessageListView(generics.ListAPIView):
    queryset = CEOMessage.objects.filter(is_active=True).order_by('-updated_at')
    serializer_class = CEOMessageSerializer     