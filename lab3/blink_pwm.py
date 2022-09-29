import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
code_run = True

# GPIO 13 is used for PWM control
GPIO.setup(13, GPIO.OUT)

# initialize f and duty cycle
frequency = 50
dc = 50

while code_run:
    # initial frequency is 1Hz
    p = GPIO.PWM(13, frequency)

    # initial duty cycle is 50%
    p.start(dc)

    # quit the program when button 27 pressed
    if not GPIO.input(27):
        code_run = False

p.stop()
GPIO.cleanup()

