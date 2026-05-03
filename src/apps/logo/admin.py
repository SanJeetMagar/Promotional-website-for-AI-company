from django.contrib import admin
from .models import Logo
@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('image', 'created_at')
    search_fields = ('image',)
    list_filter = ('created_at',)