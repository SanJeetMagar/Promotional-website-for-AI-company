from django.contrib import admin
from django.utils.html import format_html
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 'name', 'company_name', 'email', 
        'preview_priority', 'preview_status', 'created_at'
    ]
    list_filter = ['status', 'priority', 'created_at', 'product']
    search_fields = ['name', 'email', 'subject', 'message', 'company_name']
    list_editable = ['status'] # Allows you to change status directly from the list view!
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = [
        ('Contact Information', {
            'fields': (('name', 'email'), ('phone', 'company_name'))
        }),
        ('Inquiry Details', {
            'fields': ('product', 'subject', 'message')
        }),
        ('Management (Admin Only)', {
            'fields': (('priority', 'status'),),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': (('created_at', 'updated_at'),),
            'classes': ('collapse',)
        })
    ]

    # Custom colored badge for Priority
    @admin.display(description='Priority', ordering='priority')
    def preview_priority(self, obj):
        colors = {
            'LOW': 'gray',
            'MEDIUM': '#f59e0b', # Orange
            'HIGH': '#dc2626'    # Red
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_priority_display()
        )

    # Custom colored badge for Status
    @admin.display(description='Status', ordering='status')
    def preview_status(self, obj):
        colors = {
            'NEW': '#2563eb',          # Blue
            'IN_PROGRESS': '#ca8a04',  # Yellow
            'RESOLVED': '#16a34a',     # Green
            'CLOSED': 'gray'           # Gray
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; border: 1px solid {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color, color, obj.get_status_display()
        )