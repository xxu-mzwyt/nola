import json
import csv

csvFilePath = "models_data_back.csv"
jsonFilePath = "models_data_back.json"

mode = "back"

if mode == "front":
    data = []
else:
    data = {}

with open(csvFilePath, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    cnt = 1
    for row in reader:

        if cnt > 100000:
            break

        if mode == "front":

            jsonrow = {}

            for item in row:

                if item == "option_1":
                    jsonrow['option'] = []
                if "option" in item:
                    jsonrow['option'].append(row[item])

                else:
                    jsonrow[item] = row[item]

            data.append(jsonrow)

        else:
            data[str(cnt)] = row
        
        cnt += 1

with open(jsonFilePath, 'w') as jsonf:
    jsonf.write(json.dumps(data, indent=4))