from django.contrib import admin
from .models import TeamMember, CEOMessage

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position','order')
    search_fields = ('name', 'position')
    list_display_links = ['name']  # ← makes name clickable instead of id

@admin.register(CEOMessage)
class CEOMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ceo_name', 'is_active')
