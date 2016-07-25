import os
import django
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("base_dir is", BASE_DIR)

sys.path.append(BASE_DIR)
# sys.path.append('/explicit/path/to')

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'melol.settings'

django.setup()

from main.models import Platform

with open(BASE_DIR+"/pyscripts/dg_metro.json") as data_file:
    data = json.load(data_file)

# pprint(data['3']['칠곡경대병원'])
for line, p_dict in data.items():
    for platform, t_table in p_dict.items():
        Platform.objects.create(name=platform, line=line, time_table=str(t_table))
platform_list = Platform.objects.all()
platform_list.delete()