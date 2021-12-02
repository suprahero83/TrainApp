import RPi.GPIO as GPIO          
from time import sleep
import signal
import sys
import logging
import sqlite3
import random


#setup logging file
logging.basicConfig(filename="/opt/TrainApp/trainpower.log")
logging.warning("TrainPower Application Starting")

#set to 1 to write all pin traiggers to the log
pinDebug = 0

#Setting Pins for Track1 power source
in1 = 27
in2 = 17
ena1 = 18
slowpin1 = 4
stoppin1 = 20
startstopbutton1 = 6
homebutton1 = 26
homeslowpin1 = 13
homestoppin1 = 19
reverseswitch1 = 21

#setting up Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(reverseswitch1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(slowpin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(stoppin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(startstopbutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homeslowpin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homestoppin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homebutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

p1=GPIO.PWM(ena1,100)
p1.start(0)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


# Open Database Connection
con = sqlite3.connect("/opt/TrainApp/trainpower.db")  
con.row_factory = sqlite3.Row
print(con)
logging.warning(con)
#Reset all Train Profiles to stop
cur = con.cursor()
cur.execute("SELECT * FROM trains")
trains = cur.fetchall()
for train in trains:
    cur.execute("UPDATE trains SET mode='stop' WHERE id=%s" % (train['id']))
    con.commit()

#Generate initial random number for Train Station
TrainStationRandom = random.randint(1,3)
TrainStationCoutner = 1

def TrainStart(TrainSpeed,speedcontrolpin):
    logging.warning('Train is starting')
    for startSpeed in range (0, int(TrainSpeed), 1):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        speedcontrolpin.ChangeDutyCycle(int(startSpeed))

        sleep(.2)
    logging.warning("Done Starting, Train is at full speed")

def TrainStop(TrainSpeed,speedcontrolpin):
    logging.warning('Train is Stopping')
    for stopSpeed in range (int(TrainSpeed), 0 , -1):
        speedcontrolpin.ChangeDutyCycle(int(stopSpeed))
        sleep(.1)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def TrainStation(currentSpeed,slowtime,speedcontrolpin,directionpin1,directionpin2,stoppin,LowTrackVoltage,slowspeed):
    for slowDown in range (int(currentSpeed), int(slowspeed), -1):
        speedcontrolpin.ChangeDutyCycle(int(slowDown))
        slowtimeB = int(slowtime) / int(currentSpeed)
        sleep(slowtimeB)
    
    logging.warning("Wating for stop pin for train station")
    while True:       
        sleep(.1)
        if GPIO.input(stoppin) == 1:
            logging.warning("Train station stop pin triggered")
            speedcontrolpin.ChangeDutyCycle(int(LowTrackVoltage))
            break
     
    sleep(13)
    
    for slowDown in range (int(slowspeed), int(currentSpeed), 1):
        speedcontrolpin.ChangeDutyCycle(int(slowDown))
        sleep(.2) 

    logging.warning("Done with Train Station Train is back at full speed")
    return 1

def TrainHome(currentSpeed,slowtime,speedcontrolpin,directionpin1,directionpin2,thstoppin1,thslowpin1,slowspeed):

    logging.warning('Waiting for train home slow pin')
    while True:
        if pinDebug == 1:

            if GPIO.input(slowpin1) == 1:
                logging.warning("Train Station SLOW pin was triggered")

            if GPIO.input(stoppin1) == 1:
                logging.warning("Train Station STOP pin was triggered")

            if GPIO.input(startstopbutton1) == 1:
                logging.warning("Start Stop button was pushed")

            if GPIO.input(homebutton1) == 1:
                logging.warning("Home Button was pushed")

            if GPIO.input(homeslowpin1) == 1:
                logging.warning("Train Home SLOW pin was triggered")
            
            if GPIO.input(homestoppin1) == 1:
                logging.warning("Train Home STOP pin was triggered")
            
            if GPIO.input(reverseswitch1) == 1:
                logging.warning("Reverse switch was activated")

        if GPIO.input(thslowpin1) == 1:
            logging.warning('Train home slow pin was triggered')
            for slowDown in range (int(currentSpeed), int(slowspeed), -1):
                speedcontrolpin.ChangeDutyCycle(int(slowDown))
                slowtimeB = int(slowtime) / int(currentSpeed)
                sleep(slowtimeB)
            break
    logging.warning ('Waiting for train home stop pin')    
    while True:
            if GPIO.input(thstoppin1) == 1:
                logging.warning('Train home stop pin was triggered')
                speedcontrolpin.ChangeDutyCycle(0)
                GPIO.output(directionpin1,GPIO.LOW)
                GPIO.output(directionpin2,GPIO.LOW)
                break
    logging.warning('We are stopped in the tunnel')

def TrainReverse(ReverseSpeed,speedcontrolpin):
    logging.warning("In reverse, wating for the stop/start button")
    while GPIO.input(reverseswitch1) == 1:
        if GPIO.input(startstopbutton1) == 1:
            for startSpeed in range (0, int(ReverseSpeed), 1):
                speedcontrolpin.ChangeDutyCycle(int(startSpeed))
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                sleep(.2)
            logging.warning("Done Starting, Train is at full speed")
            
    
    for stopSpeed in range (int(ReverseSpeed), 0 , -1):
        speedcontrolpin.ChangeDutyCycle(int(stopSpeed))
        sleep(.05)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

signal.signal(signal.SIGINT, signal_handler)

#Start of main loop
while True:
    sleep(.01)
    #Query the active train profiles for each track. 
    cur = con.cursor()
    cur.execute("SELECT * FROM activeprofile WHERE tracknum=1")
    track1ap = cur.fetchone()
    cur.execute("SELECT * FROM activeprofile WHERE tracknum=2")
    track2ap = cur.fetchone()

    cur.execute("SELECT * FROM trains WHERE ID = %s" % (track1ap['trainID']))
    train1 = cur.fetchone()
    #Checking if the train is running or not.
    if train1['mode'] ==  'stop':
        if train1['running'] == 1:
            TrainStop(train1['speed'],p1)
            cur.execute("UPDATE trains SET running=0 WHERE id=%s" % (track1ap['trainID']))
            con.commit()
        else:
            logging.warning("Train is stopped. Waiting for start/stop button")
            while train1['mode'] == 'stop':
                sleep(.01)
                if GPIO.input(startstopbutton1) == 1:
                    cur.execute("UPDATE trains SET mode='run',running=1 WHERE id=%s" % (track1ap['trainID']))
                    con.commit()
                    TrainStart(train1['speed'],p1)
                cur.execute("SELECT * FROM trains WHERE ID = %s" % (track1ap['trainID']))
                train1 = cur.fetchone()
                    
    elif train1['mode'] == 'run':
        if GPIO.input(startstopbutton1) == 1:
                cur.execute("UPDATE trains SET mode='stop' WHERE id=%s" % (track1ap['trainID']))
                con.commit()
        elif train1['running'] == 0:
            TrainStart(train1['speed'],p1)
            cur.execute("UPDATE trains SET running=1 WHERE id=%s" % (track1ap['trainID']))
            con.commit()
    #Checking to see if Go Home function was triggered via the web interface
    elif train1['mode'] == 'home':
        TrainHome(train1['speed'],train1['slowtime'],p1,in1,in2,homestoppin1,homeslowpin1,train1['slowspeed'])
        cur.execute("UPDATE trains SET running=0, mode='stop', running=0 WHERE id=%s" % (track1ap['trainID']))
        con.commit()

    p1.ChangeDutyCycle(int(train1['speed']))
    
    if GPIO.input(slowpin1) == 1:
        if TrainStationCoutner == TrainStationRandom:     
            logging.warning('Train just hit the Train Sation')
            TrainStationCoutner = TrainStation(train1['speed'],train1['slowtime'],p1,in1,in2,stoppin1,train1['lowtrackvoltage'],train1['slowspeed'])
            TrainStationRandom = random.randint(1,3)

        else:
            logging.warning("Train hit the Trainsation Slow Pin, but passed it becasue it wasn't it's time")
            TrainStationCoutner += 1
            sleep(1)
    
    if GPIO.input(homebutton1) == 1:
        logging.warning('Train is Going Home')
        TrainHome(train1['speed'],train1['slowtime'],p1,in1,in2,homestoppin1,homeslowpin1,train1['slowspeed'])
        cur.execute("UPDATE trains SET running=0, mode='stop' WHERE id=%s" % (track1ap['trainID']))
        con.commit()

    if GPIO.input(reverseswitch1) == 1:
        logging.warning("Reverse switch has been flipped")
        TrainStop(train1['speed'],p1)
        TrainReverse(train1['reversespeed'],p1)
        cur.execute("UPDATE trains SET mode='stop',running=0 WHERE id=%s" % (track1ap['trainID']))
        con.commit()

    if pinDebug == 1:

        if GPIO.input(slowpin1) == 1:
            logging.warning("Train Station SLOW pin was triggered")

        if GPIO.input(stoppin1) == 1:
            logging.warning("Train Station STOP pin was triggered")

        if GPIO.input(startstopbutton1) == 1:
            logging.warning("Start Stop button was pushed")

        if GPIO.input(homebutton1) == 1:
            logging.warning("Home Button was pushed")

        if GPIO.input(homeslowpin1) == 1:
            logging.warning("Train Home SLOW pin was triggered")
        
        if GPIO.input(homestoppin1) == 1:
            logging.warning("Train Home STOP pin was triggered")
        
        if GPIO.input(reverseswitch1) == 1:
            logging.warning("Reverse switch was activated")
