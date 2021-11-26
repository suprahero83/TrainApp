import sqlite3
from time import sleep

# Open Database Connection
con = sqlite3.connect("trainpower.db")

con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("UPDATE trains SET running=0,mode='stop' WHERE id=1")

con.commit()