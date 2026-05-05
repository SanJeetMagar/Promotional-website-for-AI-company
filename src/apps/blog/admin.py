from django.contrib import admin
from .models import BlogPost, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)   


    