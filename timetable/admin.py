from django.contrib import admin
from django.utils.html import format_html
from .models import RamadanDay, SiteSettings


@admin.register(RamadanDay)
class RamadanDayAdmin(admin.ModelAdmin):
    list_display = [
        'ramadan_day', 'islamic_date', 'gregorian_date',
        'day_name_en', 'day_name_ur', 'sehri_time', 'iftar_time'
    ]
    list_filter = ['day_name_en']
    search_fields = ['ramadan_day', 'gregorian_date', 'islamic_date']
    ordering = ['ramadan_day']
    
    fieldsets = (
        ('📅 Day Information', {
            'fields': ('ramadan_day', 'islamic_date', 'gregorian_date')
        }),
        ('🌍 Day Names (Multilingual)', {
            'fields': ('day_name_en', 'day_name_ur', 'day_name_hi')
        }),
        ('🕌 Prayer Times', {
            'fields': ('sehri_time', 'iftar_time')
        }),
        ('📖 Dua / Quote (Optional)', {
            'fields': ('dua_text', 'dua_translation'),
            'classes': ('collapse',)
        }),
        ('🏢 Branding', {
            'fields': ('organization_name', 'location'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('ramadan_day')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'location', 'hijri_year', 'logo_preview']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px; border-radius:4px;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = "Logo"

    fieldsets = (
        ('🏢 Organization', {
            'fields': ('organization_name', 'location', 'hijri_year', 'tagline')
        }),
        ('🖼️ Branding', {
            'fields': ('logo',)
        }),
        ('📱 Social & Contact', {
            'fields': ('contact_info', 'social_handle')
        }),
    )


# Customize admin site
admin.site.site_header = "🌙 Ramadan Timetable Admin"
admin.site.site_title = "Ramadan Admin"
admin.site.index_title = "Ramadan Timetable Management"
