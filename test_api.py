import urllib.request, json

r = urllib.request.urlopen('http://127.0.0.1:8000/api/today/')
data = json.loads(r.read())
print('TODAY API: found=' + str(data['found']))
d = data['data']
print('  Day', d['ramadan_day'], ':', d['gregorian_date'], '(', d['day_name_en'], ')')
print('  Sehri:', d['sehri_time_formatted'], ' Iftar:', d['iftar_time_formatted'])

r2 = urllib.request.urlopen('http://127.0.0.1:8000/api/schedule/')
days = json.loads(r2.read())
print('SCHEDULE API:', len(days), 'days loaded')

r3 = urllib.request.urlopen('http://127.0.0.1:8000/api/settings/')
settings = json.loads(r3.read())
print('SETTINGS API:', settings['organization_name'])
print('All APIs working!')
