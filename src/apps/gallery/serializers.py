from rest_framework import serializers
from .models import GalleryCategory, GalleryImage

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption', 'order', 'created_at']


class GalleryCategorySerializer(serializers.ModelSerializer):
    # This embeds all related images inside the category payload
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'order', 'images']
        read_only_fields = ['slug']


class BulkImageUploadSerializer(serializers.Serializer):
    """
    Custom serializer to handle multiple files sent under the 'images' key
    """
    category = serializers.PrimaryKeyRelatedField(queryset=GalleryCategory.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(), 
        write_only=True,
        help_text="Upload multiple image files here."
    )

    def create(self, validated_data):
        category = validated_data['category']
        images = validated_data['images']
        
        created_images = []
        for img in images:
            # Create a GalleryImage instance for each file uploaded
            obj = GalleryImage.objects.create(category=category, image=img)
            created_images.append(obj)
            
        return created_images