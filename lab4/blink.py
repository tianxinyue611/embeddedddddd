import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)   # Set for GPIO numbering not pin numbers...
GPIO.setup(13, GPIO.OUT) # set GPIO 13 as output to blink LED
t=0.000814
print(1/(2*t))
i = 0
while i < 10000000:
    GPIO.output(13, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(13, GPIO.LOW)
    time.sleep(t)
    i = i + 1
GPIO.cleanup()
