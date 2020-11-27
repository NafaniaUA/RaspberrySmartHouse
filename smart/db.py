import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE indicators (temperature INT, huminity INT, date DATE)')
print ("Table created successfully")
conn.close()