from django.contrib import admin
from blog.models import Tag, Blog, Comment


class TagAdmin(admin.ModelAdmin):
    """Admin class for managing Tags."""
    list_display = ('name',)


class BlogAdmin(admin.ModelAdmin):
    """Admin class for managing Blogs."""
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user__username')
    filter_horizontal = ('tags',)  # For better management of ManyToMany field in admin


class CommentAdmin(admin.ModelAdmin):
    """Admin class for managing Comments."""
    list_display = ('user', 'blog', 'created_at')
    list_filter = ('user', 'blog__title', 'created_at')
    search_fields = ('user__username', 'blog__title')


# Register models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
