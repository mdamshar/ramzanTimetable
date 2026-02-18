from django.shortcuts import render


def index(request):
    return render(request, 'timetable/index.html')


def schedule(request):
    return render(request, 'timetable/schedule.html')
