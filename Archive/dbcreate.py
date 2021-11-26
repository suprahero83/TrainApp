import sqlite3

con = sqlite3.connect("trainpower.db")
print ("Database opened successfully")

con.execute("create table trains (id INTEGER PRIMARY KEY AUTOINCREMENT, trainname TEXT NOT NULL, speed INT NOT NULL, mode TEXT NOT NULL, running INT NOT NULL, slowtime INT NOT NULL, lowtrackvoltage INT NOT NULL, slowspeed INT NOT NULL)")
print("Table created successfully")

con.close()