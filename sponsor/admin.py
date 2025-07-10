from django.contrib import admin
from .models import Sponsor
from import_export.admin import ImportExportModelAdmin

@admin.register(Sponsor)
class SponsorAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'added_by', 'created_at', "id")
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'added_by__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('added_by')

