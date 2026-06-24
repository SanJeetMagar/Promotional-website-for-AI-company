from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'image_preview', 'caption', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px;"/>', obj.image.url)
        return ""

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    inlines = [GalleryImageInline]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'category', 'caption', 'order']
    list_filter = ['category']
    list_editable = ['order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px;"/>', obj.image.url)
        return ""