import RPi.GPIO as GPIO 
from time import sleep
import adafruit_pca9685
import smbus


in1 = 27
in2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)


PCA9685_pwm = adafruit_pca9685.PCA9685()

PCA9685_pwm.set_pwm_freq(100)

GPIO.setwarnings(False)

GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)

def main():
    while True:
        PCA9685_pwm.set_pwm(0,0,25)


if __name__ == '__main__':
    main()