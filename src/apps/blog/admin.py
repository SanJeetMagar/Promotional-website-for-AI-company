from django.contrib import admin
from .models import BlogPost, Comment, Tag,KeyTakeaway, BlogImage

@admin.register(KeyTakeaway)
class KeyTakeawayAdmin(admin.ModelAdmin):
    list_display = ['content', 'blog_post']
    search_fields = ['content'] 

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog_post', 'caption', 'order']
    search_fields = ['caption']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'status', 'is_featured']
    list_filter = ['status', 'is_featured', 'published_date']
    search_fields = ['title', 'author', 'content']
    readonly_fields = ['published_date', 'slug']
    exclude = ['slug']  # ← remove slug from form entirely
    actions = ['publish_posts', 'archive_posts']

    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
    publish_posts.short_description = 'Publish selected posts'

    def archive_posts(self, request, queryset):
        for post in queryset:
            post.archive()
    archive_posts.short_description = 'Archive selected posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):   
    list_display = ['name', 'blog_post', 'published_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'content']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']    