import json
from pprint import pprint

with open('testdump.json') as data_file:
    data = json.load(data_file)

keepers = ["bee_id", "common_name", "floral_host", "latitude",
           "longitude", "dateidentified"]

final_list = []

for index, entry in enumerate(data["data"]["data"]):
    keeper_attrs = {}
    for elmnt in entry:
        if elmnt in keepers:
            keeper_attrs[elmnt] = entry[elmnt]
    final_list.append({index:keeper_attrs})

for item in final_list:
    print(item)
    print()
