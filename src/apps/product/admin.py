# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, ProductImage, ProductFeature,
    ProductStep, PricingPlan, PricingPlanFeature, ProductFAQ
)


# ─── Inlines ───────────────────────────────────────────────────────────────────
# These appear INSIDE the Product admin page

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1           # how many empty forms to show by default
    fields = ['image', 'alt_text', 'order']


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    fields = ['title', 'order']


class ProductStepInline(admin.StackedInline):
    # StackedInline because each step has more fields (number, icon, title, description)
    model = ProductStep
    extra = 1
    fields = ['step_number', 'title', 'description', 'icon', 'order']


class ProductFAQInline(admin.StackedInline):
    model = ProductFAQ
    extra = 1
    fields = ['question', 'answer', 'order']


class PricingPlanFeatureInline(admin.TabularInline):
    # This inline lives INSIDE PricingPlanAdmin, not ProductAdmin
    model = PricingPlanFeature
    extra = 1
    fields = ['description', 'order']


# ─── PricingPlan Admin ─────────────────────────────────────────────────────────
# Separate admin page for pricing plans — with its own inline for features

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    inlines = [PricingPlanFeatureInline]

    list_display = ['name', 'product', 'price', 'is_custom_price', 'is_popular', 'billing_period', 'order']
    list_filter = ['product', 'is_popular', 'billing_period', 'is_custom_price']
    list_editable = ['order', 'is_popular']
    # list_editable lets you edit directly in the list without opening each record

    fieldsets = [
        # fieldsets groups fields into sections on the edit page
        ('Plan Info', {
            'fields': ['product', 'name', 'order']
        }),
        ('Pricing', {
            'fields': ['price', 'is_custom_price', 'billing_period']
        }),
        ('Display', {
            'fields': ['is_popular']
        }),
    ]


# ─── PricingPlan Inline for Product page ──────────────────────────────────────
# Separate from PricingPlanAdmin above — this is a condensed version
# that appears INSIDE the Product admin page

class PricingPlanInline(admin.StackedInline):
    model = PricingPlan
    extra = 1
    fields = ['name', 'price', 'is_custom_price', 'is_popular', 'billing_period', 'order']
    show_change_link = True
    # show_change_link = True adds a link to open the full PricingPlan edit page
    # so admin can click through to add features to that plan


# ─── Product Admin ─────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # What columns show in the product list table
    list_display = [
        'name', 'slug', 'is_active', 'order', 'preview_badge'
    ]

    # Sidebar filters
    list_filter = ['is_active']

    # Search bar — __ means "look inside related field"
    search_fields = ['name', 'slug', 'tagline', 'description']

    # Edit directly in the list without opening the record
    list_editable = ['is_active', 'order']

    # Auto-fill slug from name as you type
    prepopulated_fields = {'slug': ('name',)}

    # All the child models that appear as sections inside Product edit page
    inlines = [
        ProductImageInline,
        ProductFeatureInline,
        ProductStepInline,
        PricingPlanInline,
        ProductFAQInline,
    ]

    # Groups fields into labeled sections on the Product edit page
    fieldsets = [
        ('Basic Info', {
            'fields': ['name', 'slug', 'badge_text', 'tagline', 'description', 'order', 'is_active']
        }),
        ('Dropdown', {
            'fields': ['dropdown_short_description'],
            'description': 'Short text shown in the nav dropdown menu'
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
            # collapse = this section is folded by default, click to expand
        }),
    ]

    # Custom column — shows badge_text with styling in the list
    @admin.display(description='Badge')
    def preview_badge(self, obj):
        if obj.badge_text:
            return format_html(
                '<span style="background:#e8f0fe; color:#1a56db; '
                'padding:2px 8px; border-radius:4px; font-size:11px;">{}</span>',
                obj.badge_text
            )
        return '—'


# ─── Register remaining models with simple config ─────────────────────────────

@admin.register(ProductFAQ)
class ProductFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'product', 'order']
    list_filter = ['product']
    search_fields = ['question', 'answer']
    list_editable = ['order']