import json

with open('dagdaId.json') as jsonFile:
    data = json.load(jsonFile)
    scanId = str(data['id'])
    print(scanId)