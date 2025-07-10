from django.contrib import admin
from .models import (
    Sponsorship, PackageBenefitItem, PlatinumItem,
    SilverItem, GoldItem, ImportantNoteItem
)
from import_export.admin import ImportExportModelAdmin


@admin.register(Sponsorship)
class SponsorshipAdmin(ImportExportModelAdmin):
    list_display = ['name','price', 'status', 'created_at', 'added_by']
    readonly_fields = ['created_at', 'updated_at', 'added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(PackageBenefitItem)
class PackageBenefitItemAdmin(ImportExportModelAdmin):
    list_display = ['item', 'added_by']
    search_fields = ['item', 'added_by']
    readonly_fields = ['added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(PlatinumItem)
class PlatinumItemAdmin(ImportExportModelAdmin):
    list_display = ['item', 'added_by']
    search_fields = ['item', 'added_by']
    readonly_fields = ['added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SilverItem)
class SilverItemAdmin(ImportExportModelAdmin):
    list_display = ['item', 'added_by']
    search_fields = ['item', 'added_by']
    readonly_fields = ['added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(GoldItem)
class GoldItemAdmin(ImportExportModelAdmin):
    list_display = ['item', 'added_by']
    search_fields = ['item', 'added_by']
    readonly_fields = ['added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ImportantNoteItem)
class ImportantNoteItemAdmin(ImportExportModelAdmin):
    list_display = ['item', 'added_by']
    search_fields = ['item', 'added_by']
    readonly_fields = ['added_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
