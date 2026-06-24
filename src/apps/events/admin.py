from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Event, EventTag, Speaker, EventSpeaker, EventAgenda,
    EventGallery, EventRegistration
)


class EventSpeakerInline(admin.TabularInline):
    model = EventSpeaker
    extra = 1
    autocomplete_fields = ['speaker']


class EventAgendaInline(admin.TabularInline):
    model = EventAgenda
    extra = 1
    autocomplete_fields = ['speaker']


class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'event_type', 'status', 'event_date',
        'event_time', 'venue_name', 'is_featured',
        'registered_count', 'view_count'
    ]
    list_filter = [
        'status', 'event_type', 'is_featured',
        'is_virtual', 'event_date'
    ]
    search_fields = ['title', 'description', 'venue_name']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    inlines = [EventSpeakerInline, EventAgendaInline, EventGalleryInline]
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'description', 'short_description',
                'event_type', 'status'
            )
        }),
        ('Date & Time', {
            'fields': (
                'event_date', 'event_time', 'end_date',
                'end_time', 'duration_minutes'
            )
        }),
        ('Location', {
            'fields': (
                'venue_name', 'venue_address', 'is_virtual',
                'virtual_link', 'map_embed_url'
            )
        }),
        ('Media', {
            'fields': ('banner_image', 'thumbnail_image')
        }),
        ('Registration', {
            'fields': (
                'max_participants', 'registration_deadline',
                'registration_fee', 'is_free',
                'external_registration_url'
            )
        }),
        ('Settings', {
            'fields': ('tags', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']

    def registered_count(self, obj):
        return obj.registrations.filter(status='confirmed').count()
    registered_count.short_description = 'Registrations'


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'company', 'is_featured']
    list_filter = ['is_featured']
    search_fields = ['name', 'title', 'company', 'bio']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(EventTag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def color_preview(self, obj):
        return format_html(
            '{}',
            obj.color,
            obj.name
        )
    color_preview.short_description = 'Color Preview'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'event', 'status',
        'registration_date', 'confirmation_code', 'attended'
    ]
    list_filter = ['status', 'attended', 'registration_date', 'event']
    search_fields = [
        'full_name', 'email', 'phone', 'confirmation_code'
    ]
    readonly_fields = ['confirmation_code', 'registration_date']
    actions = ['confirm_registrations', 'mark_as_attended']
    
    fieldsets = (
        ('Event', {
            'fields': ('event',)
        }),
        ('Participant Information', {
            'fields': (
                'full_name', 'email', 'phone',
                'company', 'job_title'
            )
        }),
        ('Registration Details', {
            'fields': (
                'status', 'registration_date',
                'confirmation_code', 'notes'
            )
        }),
        ('Post-Event', {
            'fields': ('attended', 'feedback', 'rating'),
            'classes': ('collapse',)
        }),
    )

    def confirm_registrations(self, request, queryset):
        for registration in queryset:
            registration.confirm()
        self.message_user(
            request,
            f"{queryset.count()} registrations confirmed."
        )
    confirm_registrations.short_description = "Confirm selected registrations"

    def mark_as_attended(self, request, queryset):
        queryset.update(attended=True)
        self.message_user(
            request,
            f"{queryset.count()} registrations marked as attended."
        )
    mark_as_attended.short_description = "Mark as attended"


@admin.register(EventAgenda)
class EventAgendaAdmin(admin.ModelAdmin):
    list_display = ['event', 'time', 'title', 'speaker', 'duration_minutes']
    list_filter = ['event']
    search_fields = ['title', 'description']


@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'order', 'image_preview']
    list_filter = ['event']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'