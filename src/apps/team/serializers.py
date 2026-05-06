from rest_framework import serializers
from .models import TeamMember, CEOMessage

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'position', 'photo', 'bio']       

class CEOMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEOMessage
        fields = '__all__'
                