from django.contrib import admin
# Register your models here.
from .models import Posts,UserDetail
from .forms import EntryForm

class EntryAdmin(admin.ModelAdmin):
    form = EntryForm

    list_display = ('title', 'id', 'created_at', 'author')
    prepopulated_fields = { 'slug': ['title'] }
    readonly_fields = ('created_at', 'last_modified', 'last_modified_by',)
    fieldsets = ((
        None, {
            'fields': ('title', 'tagline', 'active', 'body', 'energy', 'readtime', 'tags', 'image')
        }), (
        'Other Information', {
            'fields': ('created_at', 'author', 'last_modified', 'last_modified_by', 'slug'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()


admin.site.register(Posts, EntryAdmin)
admin.site.register(UserDetail)
