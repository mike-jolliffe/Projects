# Import database functionality
import sqlite3

# Create cursor for interaction with SQL database
conn = sqlite3.connect('bee_sightings.sqlite')
cur = conn.cursor()

cur.execute('''SELECT * FROM bee_sightings WHERE sightingstatus_id == 2''')

rows = cur.fetchall()

for row in rows:
    print(row)
