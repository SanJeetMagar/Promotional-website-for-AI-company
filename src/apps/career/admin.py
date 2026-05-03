from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)