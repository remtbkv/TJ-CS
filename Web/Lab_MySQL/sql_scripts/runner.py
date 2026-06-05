import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

# data = cur.execute("SELECT * FROM assigned_e").fetchall()
# data = cur.execute('SELECT * from assigned_q WHERE c_id=0').fetchall()
data = cur.execute("SELECT q_desc from quests INNER JOIN assigned_q WHERE c_id=0 AND quests.q_id=assigned_q.q_id").fetchall()
for i in data:
    print(i)

connection.close()
