import sqlite3

connection = sqlite3.connect('database.db')

with open('create_db.sql') as f:
    connection.executescript(f.read())

print('created table')