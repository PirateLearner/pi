from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from blogging.models import BlogContentType, BlogParent, BlogContent
from blogging.forms import PostForm
from cms.admin.placeholderadmin import FrontendEditableAdmin, PlaceholderAdmin


def mark_published(modeladmin, request, queryset):
    queryset.update(published_flag = 1)
mark_published.short_description = "Mark selected content as published"



class ParentAdmin(MPTTModelAdmin):
    fieldsets = [
                 ('',     {'fields': ['name', 'parent','slug']} ),
                 ]
    list_display = ('name', 'parent', 'level')
    list_filter = ['parent']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',), }

class ContentAdmin(FrontendEditableAdmin,PlaceholderAdmin):
    
    list_display = ('title', 'create_date', 'published_flag','publication_start')
    list_filter = ['create_date']
    search_fields = ['title']
    ordering = ['title']
    actions = [mark_published]
    prepopulated_fields = {'slug': ('title',), }
    form = PostForm
    frontend_editable_fields = ('title', 'data')
    fieldsets = [
                 ('Info',     {'fields': ['title','slug', 'data','publication_start']} ),
                 ('Other',     {'fields': ['section', 'author_id', 'published_flag', 'special_flag', 'content_type','tags']} )
                 ]

admin.site.register(BlogParent, ParentAdmin)
admin.site.register(BlogContentType)
admin.site.register(BlogContent,ContentAdmin)

