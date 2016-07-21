import os
import django
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'melol.settings'
django.setup()

from main.models import Platform

with open("pyscripts/dg_metro.json") as data_file:
    data = json.load(data_file)

# pprint(data['3']['칠곡경대병원'])
for line, p_dict in data.items():
    for platform, t_table in p_dict.items():
        Platform.objects.create(name=platform, line=line, time_table=str(t_table))
# platform_list = Platform.objects.all()
# platform_list.delete()