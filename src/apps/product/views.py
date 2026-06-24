from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from .models import Product
from .serializers import (
    ProductDropdownListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
)
from .permissions import IsAdminOrReadOnly


class ProductDropdownListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('order')
    serializer_class = ProductDropdownListSerializer

    @extend_schema(
        summary="List of products for dropdowns",
        description="Returns a lightweight list of active products, ideal for dropdown selections.",
        tags=["Product"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    @extend_schema(
        summary="Product detail",
        description="Returns detailed information about a specific product including features, steps, pricing, and FAQs.",
        tags=["Product"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Create a product",
        description="Creates a new product with optional nested images, features, steps, pricing plans, FAQs, and testimonials.",
        tags=["Product"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Update a product",
        description="Updates a product. Any nested list sent (images, features, etc.) fully replaces the existing data. Omit a field entirely to leave it unchanged.",
        tags=["Product"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'

    @extend_schema(
        summary="Delete a product",
        description="Permanently deletes a product and all its related data.",
        tags=["Product"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)