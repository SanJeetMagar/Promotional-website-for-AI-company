from .models import Logo
from .serializers import LogoSerializer
from rest_framework import generics
class LogoListView(generics.ListAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    