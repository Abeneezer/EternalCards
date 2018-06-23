import json
from pprint import pprint

allNames = []

with open('eternal-cards.json') as f:
    data = json.load(f)
    for x in range(0, len(data)):
        allNames.append([data[x]["Name"], data[x]["DetailsUrl"]])
    pprint(allNames)
