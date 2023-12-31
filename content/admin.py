from content.models import Content

from django.contrib import admin


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'owner', 'type', 'created_at', 'updated_at', 'views', 'is_published',)
    list_filter = ('owner', 'type', 'is_published',)
    search_fields = ('title', 'content',)
