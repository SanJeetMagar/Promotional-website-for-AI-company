from rest_framework import serializers
from .models import TeamMember, CEOMessage

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'position', 'photo', 'bio', 'linkedin_url', 'github_url', 'twitter_url', 'order']       

class CEOMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEOMessage
        fields = ['id', 'ceo_name', 'ceo_title', 'ceo_photo', 'quote', 'body_text', 'tagline', 'sub_tagline']
                