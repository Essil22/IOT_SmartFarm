#import sqlite3

#conn = sqlite3.connect("smartfarm.db")
#cursor = conn.cursor()

#cursor.execute("SELECT * FROM sensor_data")
#rows = cursor.fetchall()

#for row in rows:
#    print(row)

#conn.close()
import sqlite3
from datetime import datetime, timedelta
import random
import math

conn = sqlite3.connect('c:/Users/HP/Desktop/IOT/project/smartfarm.db')
cursor = conn.cursor()

now = datetime.now()
rows = []

for i in range(200):
    t = now - timedelta(minutes=i * 10)
    ts = t.strftime('%Y-%m-%d %H:%M:%S')

    temperature = round(22 + math.sin(i / 10) * 4 + random.uniform(-0.5, 0.5), 1)
    humidity    = round(60 + math.sin(i / 8)  * 10 + random.uniform(-1, 1), 1)
    moisture    = round(40 + math.sin(i / 6)  * 8  + random.uniform(-1, 1), 1)
    light       = round(700 + math.sin(i / 5) * 200 + random.uniform(-10, 10), 0)

    rows.append(('farm/temperature', str(temperature), ts))
    rows.append(('farm/humidity',    str(humidity),    ts))
    rows.append(('farm/moisture',    str(moisture),    ts))
    rows.append(('farm/light',       str(light),       ts))

cursor.executemany('''
    INSERT INTO sensor_data (topic, value, timestamp)
    VALUES (?, ?, ?)
''', rows)

conn.commit()
conn.close()
print(f"Inserted {len(rows)} rows ({len(rows)//4} readings per sensor).")