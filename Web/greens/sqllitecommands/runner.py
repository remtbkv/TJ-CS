import sqlite3

connection = sqlite3.connect('nfl.db')

cur = connection.cursor()

query1 = "SELECT * FROM stadiums INNER JOIN teams ON stadiums.s_id=teams.t_stadium WHERE s_state='California' ORDER BY t_founded"

data = cur.execute(query1).fetchall()
for i in data:
    print(i)

connection.close()
