import sqlite3
from time import sleep

# Open Database Connection
con = sqlite3.connect("trainpower.db")
while True:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM trains WHERE ID = 1")
    train1 = cur.fetchone()

    print(train1['mode'])
    print(train1['running'])

    sleep(5)
    