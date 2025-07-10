from django.contrib import admin
from .models import EnvironmentSetting

@admin.register(EnvironmentSetting)
class EnvironmentSettingAdmin(admin.ModelAdmin):
    list_display = ['setting_type', 'value']
    list_filter = ['setting_type']
    search_fields = ['value']
