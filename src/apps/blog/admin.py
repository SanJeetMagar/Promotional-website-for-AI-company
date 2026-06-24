from django.contrib import admin
from .models import BlogPost, Comment, Tag, BlogImage, KeyTakeaway


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class KeyTakeawayInline(admin.TabularInline):
    model = KeyTakeaway
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_featured', 'published_date', 'view_count']
    list_filter = ['status', 'is_featured', 'published_date', 'tags']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    inlines = [KeyTakeawayInline, BlogImageInline]
    actions = ['publish_posts', 'archive_posts']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'order', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']
    
    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
        self.message_user(request, f"{queryset.count()} posts published successfully.")
    publish_posts.short_description = "Publish selected posts"
    
    def archive_posts(self, request, queryset):
        for post in queryset:
            post.archive()
        self.message_user(request, f"{queryset.count()} posts archived successfully.")
    archive_posts.short_description = "Archive selected posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog_post', 'published_date', 'is_active']
    list_filter = ['is_active', 'published_date']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} comments approved.")
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} comments disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog_post', 'caption', 'order']
    list_filter = ['blog_post']


@admin.register(KeyTakeaway)
class KeyTakeawayAdmin(admin.ModelAdmin):
    list_display = ['blog_post', 'content', 'order']
    list_filter = ['blog_post']