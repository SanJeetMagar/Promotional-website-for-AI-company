from .models import FAQ
from rest_framework import serializers

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'