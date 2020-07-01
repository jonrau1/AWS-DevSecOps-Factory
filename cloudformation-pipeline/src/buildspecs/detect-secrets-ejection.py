import json

try:
    with open('secret-results.json') as json_file:
        data = json.load(json_file)
        if str(data['results']) != '{}':
            exit(1)
        else:
            pass
except Exception as e:
    print(e)