import RPi.GPIO as GPIO
import time

print("motor control program starts......")

# GPIO used for motor A
# GPIO ? and GPIO ? are used to control direction
AIN1 = 5
AIN2 = 6
# GPIO 13 is used for PWM control
PWMA = 13
# GPIO ? is used for standby
STB = 22

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STB, GPIO.OUT)
# for motor A
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)


# initialize f and duty cycle
frequency = 50
stop_dc = 0
half_dc = 50
full_dc = 100

# the motor should be stopped at initial
pA = GPIO.PWM(PWMA, frequency)
pA.start(0)

def clockwise(p, dc):
    p.ChangeDutyCycle(dc)
    GPIO.output(STB, GPIO.HIGH)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    return None


def counterclockwise(p, dc):
    p.ChangeDutyCycle(dc)
    GPIO.output(STB, GPIO.HIGH)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    return None

def stop():
    GPIO.output(STB, GPIO.LOW)
    return None

# main
print("stop in clockwise")
stop()
time.sleep(3)

print("half-speed in clockwise")
clockwise(pA, half_dc)
time.sleep(3)

print("full-speed in clockwise")
clockwise(pA, full_dc)
time.sleep(3)

print("stop in counterclockwise")
stop()
time.sleep(3)

print("half-speed in counterclockwise")
counterclockwise(pA, half_dc)
time.sleep(3)

print("full-speed in counterclockwise")
counterclockwise(pA, full_dc)
time.sleep(3)

print("program quit")
stop()
pA.stop()
GPIO.cleanup()
