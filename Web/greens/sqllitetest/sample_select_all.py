import sqlite3

connection = sqlite3.connect('equipment.db')

cur = connection.cursor()

data = cur.execute("SELECT * FROM equipment").fetchall()
print(data)

connection.close()

