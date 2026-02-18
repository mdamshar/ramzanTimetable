"""
Management command to seed Ramadan 2026 timetable data.
Ramadan 1447 AH - approximate dates for India (adjust times per your location)
"""

from django.core.management.base import BaseCommand
from timetable.models import RamadanDay, SiteSettings
import datetime


RAMADAN_DATA = [
    # (day, islamic_date, gregorian_date, day_en, day_ur, day_hi, sehri, iftar)
    (1,  "1 Ramadan 1447",  "2026-02-28", "Saturday",  "ہفتہ",    "शनिवार",   "05:12", "18:18"),
    (2,  "2 Ramadan 1447",  "2026-03-01", "Sunday",    "اتوار",   "रविवार",   "05:11", "18:19"),
    (3,  "3 Ramadan 1447",  "2026-03-02", "Monday",    "پیر",     "सोमवार",   "05:10", "18:20"),
    (4,  "4 Ramadan 1447",  "2026-03-03", "Tuesday",   "منگل",    "मंगलवार",  "05:09", "18:20"),
    (5,  "5 Ramadan 1447",  "2026-03-04", "Wednesday", "بدھ",     "बुधवार",   "05:08", "18:21"),
    (6,  "6 Ramadan 1447",  "2026-03-05", "Thursday",  "جمعرات",  "गुरुवार",  "05:07", "18:22"),
    (7,  "7 Ramadan 1447",  "2026-03-06", "Friday",    "جمعہ",    "शुक्रवार", "05:06", "18:22"),
    (8,  "8 Ramadan 1447",  "2026-03-07", "Saturday",  "ہفتہ",    "शनिवार",   "05:05", "18:23"),
    (9,  "9 Ramadan 1447",  "2026-03-08", "Sunday",    "اتوار",   "रविवार",   "05:04", "18:24"),
    (10, "10 Ramadan 1447", "2026-03-09", "Monday",    "پیر",     "सोमवार",   "05:03", "18:24"),
    (11, "11 Ramadan 1447", "2026-03-10", "Tuesday",   "منگل",    "मंगलवार",  "05:02", "18:25"),
    (12, "12 Ramadan 1447", "2026-03-11", "Wednesday", "بدھ",     "बुधवार",   "05:01", "18:26"),
    (13, "13 Ramadan 1447", "2026-03-12", "Thursday",  "جمعرات",  "गुरुवार",  "05:00", "18:26"),
    (14, "14 Ramadan 1447", "2026-03-13", "Friday",    "جمعہ",    "शुक्रवार", "04:59", "18:27"),
    (15, "15 Ramadan 1447", "2026-03-14", "Saturday",  "ہفتہ",    "शनिवार",   "04:58", "18:28"),
    (16, "16 Ramadan 1447", "2026-03-15", "Sunday",    "اتوار",   "रविवार",   "04:57", "18:28"),
    (17, "17 Ramadan 1447", "2026-03-16", "Monday",    "پیر",     "सोमवार",   "04:56", "18:29"),
    (18, "18 Ramadan 1447", "2026-03-17", "Tuesday",   "منگل",    "मंगलवार",  "04:55", "18:30"),
    (19, "19 Ramadan 1447", "2026-03-18", "Wednesday", "بدھ",     "बुधवार",   "04:54", "18:30"),
    (20, "20 Ramadan 1447", "2026-03-19", "Thursday",  "جمعرات",  "गुरुवार",  "04:53", "18:31"),
    (21, "21 Ramadan 1447", "2026-03-20", "Friday",    "جمعہ",    "शुक्रवार", "04:52", "18:32"),
    (22, "22 Ramadan 1447", "2026-03-21", "Saturday",  "ہفتہ",    "शनिवार",   "04:51", "18:32"),
    (23, "23 Ramadan 1447", "2026-03-22", "Sunday",    "اتوار",   "रविवार",   "04:50", "18:33"),
    (24, "24 Ramadan 1447", "2026-03-23", "Monday",    "پیر",     "सोमवार",   "04:49", "18:34"),
    (25, "25 Ramadan 1447", "2026-03-24", "Tuesday",   "منگل",    "मंगलवार",  "04:48", "18:34"),
    (26, "26 Ramadan 1447", "2026-03-25", "Wednesday", "بدھ",     "बुधवार",   "04:47", "18:35"),
    (27, "27 Ramadan 1447", "2026-03-26", "Thursday",  "جمعرات",  "गुरुवार",  "04:46", "18:36"),
    (28, "28 Ramadan 1447", "2026-03-27", "Friday",    "جمعہ",    "शुक्रवार", "04:45", "18:36"),
    (29, "29 Ramadan 1447", "2026-03-28", "Saturday",  "ہفتہ",    "शनिवार",   "04:44", "18:37"),
    (30, "30 Ramadan 1447", "2026-03-29", "Sunday",    "اتوار",   "रविवार",   "04:43", "18:38"),
]

DUAS = [
    ("اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي", "O Allah, You are Forgiving and love forgiveness, so forgive me."),
    ("رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً", "Our Lord, give us good in this world and good in the Hereafter."),
    ("رَبِّ اغْفِرْ لِي وَتُبْ عَلَيَّ إِنَّكَ أَنْتَ التَّوَّابُ الرَّحِيمُ", "My Lord, forgive me and accept my repentance. Indeed, You are the Accepting of repentance, the Merciful."),
    ("اللَّهُمَّ اهْدِنِي وَسَدِّدْنِي", "O Allah, guide me and make me steadfast."),
    ("رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا", "Our Lord, let not our hearts deviate after You have guided us."),
]


class Command(BaseCommand):
    help = 'Seed Ramadan 1447 AH (2026) timetable data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌙 Seeding Ramadan 2026 timetable data...')
        
        # Create site settings
        settings_obj, created = SiteSettings.objects.get_or_create(pk=1)
        settings_obj.organization_name = "Ramadan Timetable 1447 AH"
        settings_obj.location = "India"
        settings_obj.hijri_year = "1447"
        settings_obj.tagline = "رمضان مبارک"
        settings_obj.social_handle = "#ramadanmubarak"
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS('✅ Site settings created/updated'))

        count = 0
        for entry in RAMADAN_DATA:
            day_num, islamic, greg, day_en, day_ur, day_hi, sehri, iftar = entry
            dua_text, dua_trans = DUAS[(day_num - 1) % len(DUAS)]
            
            obj, created = RamadanDay.objects.update_or_create(
                ramadan_day=day_num,
                defaults={
                    'islamic_date': islamic,
                    'gregorian_date': datetime.date.fromisoformat(greg),
                    'day_name_en': day_en,
                    'day_name_ur': day_ur,
                    'day_name_hi': day_hi,
                    'sehri_time': datetime.time.fromisoformat(sehri),
                    'iftar_time': datetime.time.fromisoformat(iftar),
                    'dua_text': dua_text,
                    'dua_translation': dua_trans,
                    'organization_name': 'Ramadan Timetable 1447 AH',
                    'location': 'India',
                }
            )
            count += 1
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} Day {day_num}: {greg} ({day_en})')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully seeded {count} Ramadan days!'))
        self.stdout.write(self.style.SUCCESS('🌙 Ramadan Mubarak! رمضان مبارک'))
