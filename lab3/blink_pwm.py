import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
code_run = True

# GPIO 13 is used for PWM control
GPIO.setup(13, GPIO.OUT)

# initialize f and duty cycle
frequency = 1
dc = 80

# initial frequency is 1Hz
p = GPIO.PWM(13, frequency)

# initial duty cycle is 50%
p.start(dc)

while code_run:

    # quit the program when button 27 pressed
    if not GPIO.input(27):
        code_run = False

p.stop()
GPIO.cleanup()
