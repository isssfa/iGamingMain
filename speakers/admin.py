from django.contrib import admin
from .models import Speaker
from import_export.admin import ImportExportModelAdmin

@admin.register(Speaker)
class SpeakerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'role', 'company', 'added_by', 'created_at')
    search_fields = ('name', 'role', 'company')
    list_filter = ('created_at', 'added_by')
    readonly_fields = ('created_at', 'updated_at', 'added_by')

    def event_list(self, obj):
        return ", ".join(obj.get_event_list())

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
