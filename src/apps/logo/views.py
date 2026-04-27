from .models import Logo
from .serializers import LogoSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema


@extend_schema(description="Get list of logos", tags=['Logo'])    
class LogoListView(generics.ListAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    