import json
import time
from pprint import pprint
import difflib

allNames = []

with open('eternal-cards.json') as f:
    data = json.load(f)
    for x in range(0, len(data)):
        allNames.append(data[x]["Name"])
    for x in allNames:
        if(x == 'Rindra\'s Choice'):
            time.sleep(1)
            pprint(x)
