from .models import Newsletter
from rest_framework import serializers  

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']