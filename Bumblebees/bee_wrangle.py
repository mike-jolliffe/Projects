import json
from pprint import pprint

with open('testdump.json') as data_file:
    data = json.load(data_file)

keepers = ["bee_id", "common_name", "floral_host", "latitude",
           "longitude", "dateidentified"]


for entry in data["data"]["data"]:
    keeper_attrs = {}
    for elmnt in entry:
        if elmnt in keepers:
            keeper_attrs[elmnt] = entry[elmnt]
    data = {entry["bee_id"]:keeper_attrs}
    print (data)
    print()
