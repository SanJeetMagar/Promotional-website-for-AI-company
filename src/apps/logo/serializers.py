from .models import Logo
from rest_framework import serializers  

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = '__all__'  