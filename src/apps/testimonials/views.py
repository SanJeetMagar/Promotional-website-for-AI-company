from .models import Testimonial
from rest_framework import generics
from .serializers import TestimonialSerializer  
from drf_spectacular.utils import extend_schema


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer

    @extend_schema(description="Get list of testimonials", tags=['Testimonials'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
