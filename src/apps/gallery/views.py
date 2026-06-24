from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from .models import GalleryCategory, GalleryImage
from .serializers import (
    GalleryCategorySerializer, 
    GalleryImageSerializer, 
    BulkImageUploadSerializer
)

# ==========================================
# PUBLIC VIEWS
# ==========================================
@extend_schema(tags=['Gallery'], summary="Get all active categories with their images")
class PublicGalleryListView(generics.ListAPIView):
    """Returns active categories including all their nested images."""
    queryset = GalleryCategory.objects.filter(is_active=True).prefetch_related('images')
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.AllowAny]


# ==========================================
# ADMIN VIEWS (Categories)
# ==========================================
@extend_schema(tags=['Gallery (Admin)'], summary="Admin: List all categories")
class AdminCategoryListView(generics.ListCreateAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['Gallery (Admin)'], summary="Admin: Update/Delete Category")
class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


# ==========================================
# ADMIN VIEWS (Images)
# ==========================================
@extend_schema(
    tags=['Gallery (Admin)'], 
    summary="Admin: Bulk Upload Images",
    description="Upload multiple images to a specific category. Send as multipart/form-data with the key `images`."
)
class AdminBulkImageUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BulkImageUploadSerializer

    def create(self, request, *args, **kwargs):
        # DRF needs `request.FILES.getlist()` to read multiple files sent under the same key
        data = request.data.copy()
        data.setlist('images', request.FILES.getlist('images'))

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        created_images = serializer.save()

        # Return the serialized data of the newly created images
        response_serializer = GalleryImageSerializer(created_images, many=True, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Gallery (Admin)'], summary="Admin: Update/Delete a single image")
class AdminImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'