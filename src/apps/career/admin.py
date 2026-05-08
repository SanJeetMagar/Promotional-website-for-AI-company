from django.contrib import admin
from .models import CV, JobPosting, Tag

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):    
    list_display = ('title', 'location', 'employment_type', 'work_arrangement', 'status')
    prepopulated_fields = {'slug': ('title',)}  # auto-generate slug from title
    list_filter = ('status', 'employment_type', 'work_arrangement')
    search_fields = ('title', 'location', 'description')

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'years_of_experience', 'job')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('job',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)