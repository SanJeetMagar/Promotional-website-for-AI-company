from django.contrib import admin
from .models import TeamMember, CEOMessage

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    search_fields = ('name', 'position')

@admin.register(CEOMessage)
class CEOMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'is_active')
    search_fields = ('message',)