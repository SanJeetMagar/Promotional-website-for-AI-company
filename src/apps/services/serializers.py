from .models import Expertise
from rest_framework import serializers

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = ['id', 'name', 'description', 'logo']     