import RPi.GPIO as GPIO          
from time import sleep
import logging


#setup logging file
logging.basicConfig(filename="trainpower.log")


#Setting Pins for Track1 power source
RENTrack1 = 27
LENTrack1 = 17
PWMRTrack1 =12
PWMLTrack1 = 18

# RENTrack1 = 22
# LENTrack1 = 4
# PWMRTrack1 =27
# PWMLTrack1 = 17


#setting up Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(RENTrack1,GPIO.OUT)
GPIO.setup(LENTrack1,GPIO.OUT)
GPIO.setup(PWMRTrack1,GPIO.OUT)
GPIO.setup(PWMLTrack1,GPIO.OUT)

GPIO.output(RENTrack1, True)
GPIO.output(LENTrack1, True)


PWMRTrack1C=GPIO.PWM(PWMRTrack1,100)
PWMLTrack1C=GPIO.PWM(PWMLTrack1,100)
PWMRTrack1C.start(0)
PWMLTrack1C.start(0)

PWMRTrack1C.ChangeDutyCycle(0)
PWMLTrack1C.ChangeDutyCycle(0)

GPIO.output(RENTrack1, True)
GPIO.output(LENTrack1, True)

while True:

    PWMRTrack1C.ChangeDutyCycle(0)
    PWMLTrack1C.ChangeDutyCycle(0)