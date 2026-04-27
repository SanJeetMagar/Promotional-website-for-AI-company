from .models import Product
from .serializers import ProductDropdownListSerializer, ProductDetailSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema 

class ProductDropdownListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('order')
    serializer_class = ProductDropdownListSerializer

    @extend_schema(
        summary="List of products for dropdowns",
        description="Returns a lightweight list of products with minimal details, ideal for dropdown selections.",
    tags=["Product"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    @extend_schema(
        summary="Product detail",
        description="Returns detailed information about a specific product, including features, steps, pricing plans, and FAQs.", tags=["Product"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)    