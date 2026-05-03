from django.contrib import admin

from .models import ContactMessage, ContactInfo, SocialMediaLink

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'subject', 'created_at')
    search_fields = ('first_name', 'email', 'subject')
    list_filter = ('created_at',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'email', 'created_at')
    search_fields = ('address', 'phone_number', 'email')
    list_filter = ('created_at',)

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'created_at')
    search_fields = ('platform', 'url')
    list_filter = ('created_at',)