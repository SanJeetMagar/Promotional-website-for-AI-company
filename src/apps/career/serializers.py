from .models import Career
from rest_framework import serializers

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'