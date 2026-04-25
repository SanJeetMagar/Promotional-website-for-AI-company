from .models import TeamMember, CEOMessage
from .serializers import TeamMemberSerializer, CEOMessageSerializer
from rest_framework import generics     

class TeamMemberListCreateView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer 

class CEOMessageListCreateView(generics.ListCreateAPIView):
    queryset = CEOMessage.objects.filter(is_active=True).order_by('-updated_at')
    serializer_class = CEOMessageSerializer     