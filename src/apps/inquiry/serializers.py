from rest_framework import serializers
from .models import Inquiry

class PublicInquiryCreateSerializer(serializers.ModelSerializer):
    """
    Used by the public website frontend. 
    Users submit their inquiry here. Status is automatically set to 'NEW'.
    """
    class Meta:
        model = Inquiry
        fields = [
            'id', 'name', 'email', 'phone', 'company_name', 
            'product', 'subject', 'message', 'priority'
        ]
        read_only_fields = ['id']


class AdminInquirySerializer(serializers.ModelSerializer):
    """
    Used by the Custom Frontend Admin Panel.
    Includes status and timestamps. Product name is nested for easy reading.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Inquiry
        fields = [
            'id', 'name', 'email', 'phone', 'company_name', 
            'product', 'product_name', 'subject', 'message', 
            'priority', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']