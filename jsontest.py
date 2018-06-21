import json
from pprint import pprint

with open('eternal-cards.json') as f:
    data = json.load(f)
pprint(data[1052]["SetNumber"])
