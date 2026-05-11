from .models import About, VisionMission
from rest_framework import serializers  

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'description', 'image']    

class VisionMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionMission
        fields = ['id', 'title', 'description'] 