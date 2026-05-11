from .models import About, VisionMission
from .serializers import AboutSerializer, VisionMissionSerializer
from rest_framework import generics

class AboutListView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class VisionMissionListView(generics.ListAPIView):
    queryset = VisionMission.objects.all()
    serializer_class = VisionMissionSerializer

