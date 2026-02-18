from rest_framework import serializers
from .models import RamadanDay, SiteSettings


class RamadanDaySerializer(serializers.ModelSerializer):
    sehri_time_formatted = serializers.SerializerMethodField()
    iftar_time_formatted = serializers.SerializerMethodField()
    gregorian_date_display = serializers.SerializerMethodField()

    class Meta:
        model = RamadanDay
        fields = [
            'id',
            'ramadan_day',
            'islamic_date',
            'gregorian_date',
            'gregorian_date_display',
            'day_name_en',
            'day_name_ur',
            'day_name_hi',
            'sehri_time',
            'iftar_time',
            'sehri_time_formatted',
            'iftar_time_formatted',
            'dua_text',
            'dua_translation',
            'organization_name',
            'location',
        ]

    def get_sehri_time_formatted(self, obj):
        return obj.sehri_time.strftime("%I:%M %p") if obj.sehri_time else ""

    def get_iftar_time_formatted(self, obj):
        return obj.iftar_time.strftime("%I:%M %p") if obj.iftar_time else ""

    def get_gregorian_date_display(self, obj):
        if obj.gregorian_date:
            return obj.gregorian_date.strftime("%d %B %Y")
        return ""


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = ['id', 'organization_name', 'location', 'logo', 'logo_url',
                  'hijri_year', 'tagline', 'contact_info', 'social_handle']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None
