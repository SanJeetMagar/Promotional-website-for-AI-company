from django.contrib import admin
from django.utils.html import format_html
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 
        'name', 
        'company_name', 
        'email', 
        'preview_priority', 
        'status',      # <--- This must be here for list_editable to work
        'created_at'
    ]
    list_filter = ['status', 'priority', 'created_at', 'product']
    search_fields = ['name', 'email', 'subject', 'message', 'company_name']
    list_editable = ['status'] 
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