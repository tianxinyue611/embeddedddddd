import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# GPIO used for motor A
# GPIO 5 and GPIO 6 are used to control direction
AIN1 = 5
AIN2 = 6
# GPIO 13 is used for PWM control
PWMA = 13
# GPIO used for motor B
# GPIO 22 and GPIO 27 are used to control direction
BIN1 = 24
BIN2 = 25
PWMB = 18

# Set up GPIO
GPIO.setmode(GPIO.BCM)
# 17 is used to switch between motor A and motor B
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 22 is used to let motor run clockwise
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 23 is used to let motor run counterclockwise
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 27 is used to stop the motor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# for motor A
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

# for motor B
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)


# initialize f and duty cycle
frequency = 50
stop_dc = 0
half_dc = 50
full_dc = 100

# the motor should be stopped at initial
pA = GPIO.PWM(PWMA, frequency)
pA.start(0)
pB = GPIO.PWM(PWMB, frequency)
pB.start(0)
p = pA

# function to control motors
def clockwise(p, dc, in1, in2):
    p.ChangeDutyCycle(dc)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    return None


def counterclockwise(p, dc, in1, in2):
    p.ChangeDutyCycle(dc)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    return None

def stop(p):
    p.ChangeDutyCycle(0)
    return None

start_time = time.time()
code_run = True
while code_run:
    time.sleep(0.2)  # Without sleep, no screen output!
    
    if ( not GPIO.input(17) ):
        if p==pA:
            p = pB
        elif p==pB:
            p = pA
            
    if ( not GPIO.input(22) ):
        if(p==pA):
            clockwise(p, half_dc, AIN1, AIN2)
        if(p==pB):
            clockwise(p, half_dc, BIN1, BIN2)
        
    if (not GPIO.input(23)):
        if(p==pA):
            counterclockwise(p, half_dc, AIN1, AIN2)
        if(p==pB):
            counterclockwise(p, half_dc, BIN1, BIN2)
            
    if (not GPIO.input(27)):
        stop(p)
        
    if time.time()-start_time>30:
        code_run = False
        
    
pA.stop()
pB.stop()

GPIO.output(AIN2, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)

GPIO.cleanup() 