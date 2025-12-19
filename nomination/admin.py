from django.contrib import admin
from .models import Nomination
from import_export.admin import ImportExportModelAdmin


@admin.register(Nomination)
class NominationAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'email', 'company', 'nominated_company', 'award_category', 'email_sent', 'created_at')
    search_fields = ('full_name', 'email', 'company', 'nominated_company', 'award_category')
    list_filter = ('award_category', 'email_sent', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'email_sent')
    fieldsets = (
        ('Nominator Information', {
            'fields': ('full_name', 'email', 'phone_number', 'company', 'role')
        }),
        ('Nomination Details', {
            'fields': ('nominated_company', 'award_category', 'reason_for_nomination')
        }),
        ('Status', {
            'fields': ('email_sent', 'created_at', 'updated_at')
        }),
    )

