from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product
from .serializers import (
    ProductDropdownListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
)
from .permissions import IsAdminOrReadOnly


@extend_schema_view(
    get=extend_schema(
        summary="List of products for dropdowns",
        description="Returns a lightweight list of active products, ideal for dropdown selections.",
        tags=["Product"],
    )
)
class ProductDropdownListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('order')
    serializer_class = ProductDropdownListSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Product detail",
        description="Returns detailed information about a specific product including features, steps, pricing, and FAQs.",
        tags=["Product"],
    )
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


@extend_schema_view(
    post=extend_schema(
        summary="Create a product",
        description="Creates a new product with optional nested images, features, steps, pricing plans, FAQs, and testimonials.",
        tags=["Product"],
    )
)
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


@extend_schema_view(
    put=extend_schema(
        summary="Update a product (Full)",
        description="Fully replaces the product. Nested lists fully replace existing data.",
        tags=["Product"],
    ),
    patch=extend_schema(
        summary="Update a product (Partial)",
        description="Partially updates a product. Omit a field entirely to leave it unchanged.",
        tags=["Product"],
    )
)
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]


@extend_schema_view(
    delete=extend_schema(
        summary="Delete a product",
        description="Permanently deletes a product and all its related data.",
        tags=["Product"],
    )
)
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'