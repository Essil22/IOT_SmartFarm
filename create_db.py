#import sqlite3

#conn = sqlite3.connect("smartfarm.db")

#cursor = conn.cursor()

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS sensor_data (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
 #   topic TEXT,
  #  value TEXT,
   # timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

#""")

#conn.commit()
#conn.close()

#print("Database created successfully!")
import sqlite3

conn = sqlite3.connect('smartfarm.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity    REAL,
        moisture    REAL,
        light       REAL,
        timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database created: smartfarm.db")