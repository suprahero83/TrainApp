#Used to update current db to add reverse speed into trains table

import sqlite3

con=sqlite3.connect('/opt/TrainApp/trainpower.db')
con.row_factory = sqlite3.Row
cur=con.cursor()

reversespeed = 0

con.execute("create table trainsTMP (id INTEGER PRIMARY KEY AUTOINCREMENT, trainname TEXT NOT NULL, speed INT NOT NULL, mode TEXT NOT NULL, running INT NOT NULL, slowtime INT NOT NULL, lowtrackvoltage INT NOT NULL, slowspeed INT NOT NULL)")

cur.execute("SELECT * FROM trains")
trains = cur.fetchall()

for train in trains:
    cur.execute("INSERT into trainsTMP (trainname, speed, mode, running, slowtime, lowtrackvoltage, slowspeed) values (?,?,?,?,?,?,?)",(train['trainname'],train['speed'],train['mode'],train['running'],train['slowtime'],train['lowtrackvoltage'],train['slowspeed']))

con.commit()

cur.execute("DROP TABLE trains")
con.execute("create table trains (id INTEGER PRIMARY KEY AUTOINCREMENT, trainname TEXT NOT NULL, speed INT NOT NULL, mode TEXT NOT NULL, running INT NOT NULL, slowtime INT NOT NULL, lowtrackvoltage INT NOT NULL, slowspeed INT NOT NULL, reversespeed INT NOT NULL)")


cur.execute("SELECT * FROM trainsTMP")
trains = cur.fetchall()

for train in trains:
    cur.execute("INSERT into trains (trainname, speed, mode, running, slowtime, lowtrackvoltage, slowspeed, reversespeed) values (?,?,?,?,?,?,?,?)",(train['trainname'],train['speed'],train['mode'],train['running'],train['slowtime'],train['lowtrackvoltage'],train['slowspeed'],reversespeed))

con.commit()

cur.execute("DROP TABLE trainsTMP")


con.close()










