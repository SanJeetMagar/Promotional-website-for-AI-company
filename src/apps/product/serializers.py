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


class PricingPlanWriteSerializer(serializers.ModelSerializer):
    pricing_features = PricingPlanFeatureSerializer(many=True, required=False)

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


class ProductTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTestimonial
        fields = ['id', 'author_name', 'author_title', 'content', 'order', 'author_profile_image']


class ProductDropdownListSerializer(serializers.ModelSerializer):
    """Lightweight — for dropdown and list views."""
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'tagline',
            'dropdown_short_description', 'order',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Heavy read-only — for single product detail page only."""
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


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Writable — for create and update operations."""
    images = ProductImageSerializer(many=True, required=False)
    features = ProductFeatureSerializer(many=True, required=False)
    steps = ProductStepSerializer(many=True, required=False)
    pricing_plans = PricingPlanWriteSerializer(many=True, required=False) 
    faqs = ProductFAQSerializer(many=True, required=False)
    testimonials = ProductTestimonialSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'badge_text', 'tagline',
            'description', 'dropdown_short_description',
            'meta_title', 'meta_description', 'is_active', 'order',
            'images', 'features', 'steps', 'pricing_plans', 'faqs', 'testimonials',
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        features_data = validated_data.pop('features', [])
        steps_data = validated_data.pop('steps', [])
        pricing_plans_data = validated_data.pop('pricing_plans', [])
        faqs_data = validated_data.pop('faqs', [])
        testimonials_data = validated_data.pop('testimonials', [])

        product = Product.objects.create(**validated_data)

        for data in images_data:
            ProductImage.objects.create(product=product, **data)

        for data in features_data:
            ProductFeature.objects.create(product=product, **data)

        for data in steps_data:
            ProductStep.objects.create(product=product, **data)

        for plan_data in pricing_plans_data:
            plan_features_data = plan_data.pop('pricing_features', [])
            plan = PricingPlan.objects.create(product=product, **plan_data)
            for pf_data in plan_features_data:
                # Fixed bug: The model field is 'pricing_plan', not 'plan'
                PricingPlanFeature.objects.create(pricing_plan=plan, **pf_data)

        for data in faqs_data:
            ProductFAQ.objects.create(product=product, **data)

        for data in testimonials_data:
            ProductTestimonial.objects.create(product=product, **data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        features_data = validated_data.pop('features', None)
        steps_data = validated_data.pop('steps', None)
        pricing_plans_data = validated_data.pop('pricing_plans', None)
        faqs_data = validated_data.pop('faqs', None)
        testimonials_data = validated_data.pop('testimonials', None)

        # Update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data is not None:
            instance.images.all().delete()
            for data in images_data:
                ProductImage.objects.create(product=instance, **data)

        if features_data is not None:
            instance.features.all().delete()
            for data in features_data:
                ProductFeature.objects.create(product=instance, **data)

        if steps_data is not None:
            instance.steps.all().delete()
            for data in steps_data:
                ProductStep.objects.create(product=instance, **data)

        if pricing_plans_data is not None:
            instance.pricing_plans.all().delete()
            for plan_data in pricing_plans_data:
                plan_features_data = plan_data.pop('pricing_features', [])
                plan = PricingPlan.objects.create(product=instance, **plan_data)
                for pf_data in plan_features_data:
                    # Fixed bug: The model field is 'pricing_plan', not 'plan'
                    PricingPlanFeature.objects.create(pricing_plan=plan, **pf_data)

        if faqs_data is not None:
            instance.faqs.all().delete()
            for data in faqs_data:
                ProductFAQ.objects.create(product=instance, **data)

        if testimonials_data is not None:
            instance.testimonials.all().delete()
            for data in testimonials_data:
                ProductTestimonial.objects.create(product=instance, **data)

        return instance