from .models import ContactMessage, ContactInfo
from rest_framework import serializers  

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'


# class SocialMediaLinkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SocialMediaLink
#         fields = '__all__'