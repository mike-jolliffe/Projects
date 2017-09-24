# imports
import sqlite3
import requests
import json

# decode the json
with open('bee_sightings.json') as fh:
    js = json.load(fh)

# clean up the dictionary by eliminating the outermost key
data = []
for item in js:
    data.extend([value for (key,value) in item.items()])

# flatten dateidentified from dict of dicts, grab just date
for item in data:
    item["dateidentified"] = item["dateidentified"]["date"]

# create a new database file and generate a cursor for SQL execution
conn = sqlite3.connect('bee_sightingsPK.sqlite')
cur = conn.cursor()

# create a table for the data
cur.execute('''CREATE table bee_sightings(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               bee_id INTEGER, common_name TEXT, dateidentified DATETIME,
               latitude REAL, longitude REAL, floral_host TEXT,
               sightingstatus_id INTEGER)''')

# Insert data into the table
cur.executemany('''INSERT INTO bee_sightings(bee_id, common_name, dateidentified,
                  latitude, longitude, floral_host, sightingstatus_id) VALUES
                  (:bee_id, :common_name, :dateidentified, :latitude, :longitude,
                  :floral_host, :sightingstatus_id)''', data)

# Save the changes and close the connection
conn.commit()
conn.close()
