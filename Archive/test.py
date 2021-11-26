import logging
import RPi.GPIO as GPIO          
from time import sleep

logging.basicConfig(filename="Archive/test.log")

slowpin1 = 4
stoppin1 = 20
startstopbutton1 = 6
homebutton1 = 26
homeslowpin1 = 13
homestoppin1 = 19
reverseswitch1 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(reverseswitch1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(slowpin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(stoppin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(startstopbutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homeslowpin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homestoppin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(homebutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

i=0

while True:

    print (GPIO.input(slowpin1))
    print (GPIO.input(stoppin1))
    print ("break")    

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
    
    sleep(1)
    logging.warning("New Loop")

    i += 1
    logging.warning(i)
