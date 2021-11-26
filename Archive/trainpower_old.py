#TODO: Create go home routine, needs own perameters in trainprofile
#TODO: Create reverse routine, Switch to execute function to slow the train and reverse. 
#TODO: replicate to second track
#TODO: Lowtrackvolate Variable in TrainProfile.json
#TODO: Reverse speed in TrainProfile.json



import RPi.GPIO as GPIO          
from time import sleep
import json
import signal
import sys
import logging


#setup logging file
logging.basicConfig(filename="trainpower.log")


#Setting Pins for Track1 power source
in1 = 27
in2 = 17
ena1 = 22
slowpin1 = 18
stoppin1 = 20
startstopbutton1 = 6
homebutton1 = 26
homeslowpin1 = 13
homestopping1 = 19
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
GPIO.setup(homestopping1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homebutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


p1=GPIO.PWM(ena1,1000)
p1.start(0)


running1 = '0'  
#Load Last Settings
f = open('/opt/TrainPower/settings.json',)
settings=json.load(f)
TrackProfile1=(settings['TrackProfile1'])
f.close()

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

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
     
    sleep(17)
    
    for slowDown in range (int(slowspeed), int(currentSpeed), 1):
        speedcontrolpin.ChangeDutyCycle(int(slowDown))
        sleep(.2) 


def TrainHome(currentSpeed,slowtime,speedcontrolpin,directionpin1,directionpin2,stoppin,slowpin,slowspeed):
    logging.warning('Waiting For slow pin for train home')
    while True:
        if GPIO.input(slowpin) == 1:
            logging.warning('Train home slow pin was triggered')
            for slowDown in range (int(currentSpeed), int(slowspeed), -1):
                speedcontrolpin.ChangeDutyCycle(int(slowDown))
                slowtimeB = int(slowtime) / int(currentSpeed)
                sleep(slowtimeB)
            break
    logging.warning ('wating for stop pin for train home')    
    while True:
            if GPIO.input(stoppin) == 1:
                logging.warning('Train home stop pin was triggered')
                speedcontrolpin.ChangeDutyCycle(0)
                GPIO.output(directionpin1,GPIO.LOW)
                GPIO.output(directionpin2,GPIO.LOW)
                break
    logging.warning('We are stopped in the tunnel')

def TrainReverse (currentSpeed,speedcontrolpin,directionpin1,directionpin2,ReverseSwitch,ReverseSpeed):
    
    logging.warning (GPIO.input(reverseswitch1))
    for stopSpeed in range (int(currentSpeed), 0 , -1):
        speedcontrolpin.ChangeDutyCycle(int(stopSpeed))
        sleep(.1)
    GPIO.output(directionpin1,GPIO.LOW)
    GPIO.output(directionpin2,GPIO.LOW)
    

    sleep(1)
    GPIO.output(directionpin1,GPIO.LOW)
    GPIO.output(directionpin2,GPIO.HIGH)

    for startSpeed in range (0, int(ReverseSpeed), 1):
        speedcontrolpin.ChangeDutyCycle(int(startSpeed))
        sleep(.2)
    
    while GPIO.input(ReverseSwitch) == 1:
        if GPIO.input(ReverseSwitch) == 0:
            break
    
    for stopSpeed in range (int(ReverseSpeed), 0 , -1):
        speedcontrolpin.ChangeDutyCycle(int(stopSpeed))
        sleep(.1)
    GPIO.output(directionpin1,GPIO.LOW)
    GPIO.output(directionpin2,GPIO.LOW)
    

    sleep(1)
    for startSpeed in range (0, int(currentSpeed), 1):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        speedcontrolpin.ChangeDutyCycle(int(startSpeed))
        sleep(.2)


    
        

def TrainStart(TrainSpeed,speedcontrolpin):
    
    for startSpeed in range (0, int(TrainSpeed), 1):
        speedcontrolpin.ChangeDutyCycle(int(startSpeed))
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(.2)
    return '1'

def TrainStop(TrainSpeed,speedcontrolpin):
    
    for stopSpeed in range (int(TrainSpeed), 0 , -1):
        speedcontrolpin.ChangeDutyCycle(int(stopSpeed))
        sleep(.1)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    return '0'

signal.signal(signal.SIGINT, signal_handler)

#Start of main loop
while True:



    profileSettings1 = open(TrackProfile1)
    sleep(.05)
    profileData1=json.load(profileSettings1)
    speed1 = (profileData1['speed'])
    mode1 = (profileData1['mode'])
    slowtime1 = (profileData1['slowtime'])
    reversespeed1 = (profileData1['reversespeed'])
    lowtrackvoltage1 = (profileData1['lowtrackvoltage'])
    slowspeed1 = (profileData1['slowspeed'])

    if mode1 == 'stop':
        logging.warning ('running ' + running1)
        if running1 == '1':
            running1 = TrainStop(speed1,p1)
            
        else:
            while mode1 == 'stop':
                profileSettings1 = open(TrackProfile1)
                profileData1=json.load(profileSettings1)
                mode1 = (profileData1['mode'])
                trainName1 = (profileData1['TrainName'])
                speed1 = (profileData1['speed'])
                reversespeed1 = (profileData1['reversespeed'])
                lowtrackvoltage1 = (profileData1['lowtrackvoltage'])
                slowtime1 = (profileData1['slowtime'])
                slowspeed1 = (profileData1['slowspeed'])
                running1 = '0'
                

                if GPIO.input(startstopbutton1) == 1:
                    data1 = '{\r \
"TrainName" : "' + trainName1 +'",\r \
"speed" : "' + speed1 +'",\r \
"mode" : "run",\r \
"running" : "' + running1 +'",\r \
"slowtime" : "' + slowtime1 +'",\r \
"reversespeed" : "' + reversespeed1 +'",\r \
"lowtrackvoltage" : "' + lowtrackvoltage1 +'",\r \
"slowspeed" : "' + slowspeed1 +'"\r \
}'

                    with open (TrackProfile1, 'w') as outfile1:
                        outfile1.write(data1)
                    outfile1.close()
                sleep(.07)

    elif mode1=='run':
        
        if GPIO.input(startstopbutton1) == 1:
            profileSettings1 = open(TrackProfile1)
            profileData1=json.load(profileSettings1)
            mode1 = (profileData1['mode'])
            trainName1 = (profileData1['TrainName'])
            speed1 = (profileData1['speed'])
            running1 = '1'
            slowtime1 = (profileData1['slowtime'])
            reversespeed1 = (profileData1['reversespeed'])
            lowtrackvoltage1 = (profileData1['lowtrackvoltage'])
            slowspeed1 = (profileData1['slowspeed'])
            data1 = '{\r \
"TrainName" : "' + trainName1 +'",\r \
"speed" : "' + speed1 +'",\r \
"mode" : "stop",\r \
"running" : "' + running1 +'",\r \
"slowtime" : "' + slowtime1 +'",\r \
"reversespeed" : "' + reversespeed1 +'",\r \
"lowtrackvoltage" : "' + lowtrackvoltage1 +'",\r \
"slowspeed" : "' + slowspeed1 +'"\r \
}'
            with open (TrackProfile1, 'w') as outfile1:
                outfile1.write(data1)
            outfile1.close()
            sleep(.5)
        elif running1 == '0':
            running1 = TrainStart(speed1,p1)

    p1.ChangeDutyCycle(int(speed1))

    

    if GPIO.input(slowpin1) == 1:
        logging.warning('We just hit the Train Sation')
        TrainStation(speed1,slowtime1,p1,in1,in2,stoppin1,lowtrackvoltage1,slowspeed1)

    if GPIO.input(homebutton1) == 1:
        logging.warning('We Going Home')
        TrainHome(speed1,slowtime1,p1,in1,in2,homestopping1,homeslowpin1,slowspeed1)
        profileSettings1 = open(TrackProfile1)
        profileData1=json.load(profileSettings1)
        mode1 = (profileData1['mode'])
        trainName1 = (profileData1['TrainName'])
        speed1 = (profileData1['speed'])
        running1 = '0'
        slowtime1 = (profileData1['slowtime'])
        reversespeed1 = (profileData1['reversespeed'])
        lowtrackvoltage1 = (profileData1['lowtrackvoltage'])
        slowspeed1 = (profileData1['slowspeed'])
        data1 = '{\r \
"TrainName" : "' + trainName1 +'",\r \
"speed" : "' + speed1 +'",\r \
"mode" : "stop",\r \
"running" : "' + running1 +'",\r \
"slowtime" : "' + slowtime1 +'",\r \
"reversespeed" : "' + reversespeed1 +'",\r \
"lowtrackvoltage" : "' + lowtrackvoltage1 +'",\r \
"slowspeed" : "' + slowspeed1 +'"\r \
}'
        with open (TrackProfile1, 'w') as outfile1:
            outfile1.write(data1)
        outfile1.close()
        sleep(.5)
        


