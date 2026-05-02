from rest_framework import serializers
from .models import (
    Product, ProductImage, ProductFeature,
    ProductStep, PricingPlan, PricingPlanFeature, ProductFAQ, ProductTestimonial
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'title', 'order']


class ProductStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStep
        fields = ['id', 'step_number', 'icon', 'title', 'description', 'order']


class PricingPlanFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlanFeature
        fields = ['id', 'description', 'order']


class PricingPlanSerializer(serializers.ModelSerializer):
    pricing_features = PricingPlanFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'price', 'is_custom_price',
            'is_popular', 'billing_period', 'order',
            'pricing_features',
        ]


class ProductFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ['id', 'question', 'answer', 'order']


class ProductDropdownListSerializer(serializers.ModelSerializer):
    """Lightweight — for dropdown and list views."""
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'tagline',
            'dropdown_short_description', 'order',
        ]

class ProductTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTestimonial
        fields = ['id', 'author_name', 'author_title', 'content', 'order', 'author_profile_image']
class ProductDetailSerializer(serializers.ModelSerializer):
    """Heavy — for single product detail page only."""
    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    steps = ProductStepSerializer(many=True, read_only=True)
    pricing_plans = PricingPlanSerializer(many=True, read_only=True)
    faqs = ProductFAQSerializer(many=True, read_only=True)
    testimonials = ProductTestimonialSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'badge_text', 'tagline',
            'description', 'meta_title', 'meta_description',
            'is_active', 'order',
            'images', 'features', 'steps', 'pricing_plans', 'faqs', 'testimonials',
        ]