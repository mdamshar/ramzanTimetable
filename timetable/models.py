from django.db import models


class RamadanDay(models.Model):
    ramadan_day = models.PositiveIntegerField(unique=True, verbose_name="Ramadan Day Number")
    
    # Islamic date
    islamic_date = models.CharField(max_length=100, verbose_name="Islamic Date (e.g. 1 Ramadan 1447)")
    
    # Gregorian date
    gregorian_date = models.DateField(verbose_name="Gregorian Date")
    
    # Day names in multiple languages
    day_name_en = models.CharField(max_length=20, verbose_name="Day Name (English)")
    day_name_ur = models.CharField(max_length=50, verbose_name="Day Name (Urdu)", blank=True)
    day_name_hi = models.CharField(max_length=50, verbose_name="Day Name (Hindi)", blank=True)
    
    # Prayer times
    sehri_time = models.TimeField(verbose_name="Sehri Time (End)")
    iftar_time = models.TimeField(verbose_name="Iftar Time")
    
    # Optional dua
    dua_text = models.TextField(blank=True, verbose_name="Dua / Quote (Optional)")
    dua_translation = models.TextField(blank=True, verbose_name="Dua Translation (Optional)")
    
    # Branding
    organization_name = models.CharField(max_length=200, blank=True, default="Ramadan Timetable 1447 AH")
    location = models.CharField(max_length=100, blank=True, default="India")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ramadan_day']
        verbose_name = "Ramadan Day"
        verbose_name_plural = "Ramadan Days"

    def __str__(self):
        return f"Day {self.ramadan_day} - {self.gregorian_date} ({self.day_name_en})"

    def sehri_time_formatted(self):
        return self.sehri_time.strftime("%I:%M %p")

    def iftar_time_formatted(self):
        return self.iftar_time.strftime("%I:%M %p")


class SiteSettings(models.Model):
    organization_name = models.CharField(max_length=200, default="Ramadan Timetable 1447 AH")
    location = models.CharField(max_length=100, default="India")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    hijri_year = models.CharField(max_length=10, default="1447")
    tagline = models.CharField(max_length=300, blank=True, default="رمضان مبارک")
    contact_info = models.CharField(max_length=300, blank=True)
    social_handle = models.CharField(max_length=100, blank=True, default="#ramadanmubarak")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Settings - {self.organization_name}"
