from pprint import pprint
import json

with open("dg_metro.json") as data_file:
    data = json.load(data_file)

pprint(data['3']['칠곡경대병원'])