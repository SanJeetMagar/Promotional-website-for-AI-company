from django.db import models
from src.apps.common.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    badge_text = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    tagline = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    dropdown_short_description = models.CharField(max_length=155,blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} Image"
class ProductFeature(BaseModel):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # icon = models.ImageField(upload_to='product/feature_icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)  
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.product.name} - {self.title}"

class ProductStep(BaseModel):
    product = models.ForeignKey(Product, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    icon = models.ImageField(upload_to='product/step_icons/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.product.name} - {self.title}"
    

class PricingPlan(BaseModel):
    product = models.ForeignKey(Product, related_name='pricing_plans', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_custom_price = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    billing_period = models.CharField(
        max_length=20,
        choices=[('month', 'Monthly'), ('year', 'Yearly')],
        default='month'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
class PricingPlanFeature(BaseModel):
    pricing_plan = models.ForeignKey(PricingPlan, related_name='pricing_features', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)  
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.pricing_plan.name} - {self.description}"
    

class ProductFAQ(BaseModel):
    product = models.ForeignKey(Product, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)  
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.product.name} - {self.question[:50]}"
    
class ProductTestimonial(BaseModel):
    product = models.ForeignKey(Product, related_name='testimonials', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255, blank=True)
    author_profile_image = models.ImageField(upload_to='product/testimonials/', blank=True, null=True)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)  
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.product.name} - Testimonial by {self.author_name}"