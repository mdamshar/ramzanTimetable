from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'days', views.RamadanDayViewSet, basename='ramadanday')

urlpatterns = [
    path('', include(router.urls)),
    path('today/', views.get_today_timetable, name='today-timetable'),
    path('schedule/', views.get_all_timetable, name='full-schedule'),
    path('day/<int:day_number>/', views.get_day_by_number, name='day-by-number'),
    path('settings/', views.get_site_settings, name='site-settings'),
    path('countdown/', views.get_iftar_countdown, name='iftar-countdown'),
]
