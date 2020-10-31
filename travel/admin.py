from django.contrib import admin
from .models import Post, Comment, DataTracking
myModels = [Comment, DataTracking]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
class DataTrackingAdmin(admin.ModelAdmin):
    list_display = ('blogtitle','country','viewcount')
    list_filter = ('blogtitle','country')
    search_fields = ('blogtitle','country','viewcount')
admin.site.register(DataTracking, DataTrackingAdmin)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js=("injectjs.js",)
    list_display = ('title', 'slug', 'status','created_on','tag_let_one')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)
