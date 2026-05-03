from .models import Career
from .serializers import CareerSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema


@extend_schema(description="List all career opportunities", tags=['Career'],summary="List of career opportunities")
class CareerListView(generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')