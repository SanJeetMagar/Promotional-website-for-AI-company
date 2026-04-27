from .models import Expertise
from .serializers import ExpertiseSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="List of Expertise",
    description="Retrieve a list of all expertise areas offered by the company.",
    tags=["Services"],
)
class ExpertiseListView(generics.ListAPIView):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer  