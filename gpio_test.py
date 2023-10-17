import RPi.GPIO as GPIO
import time

print("Setting Up")
GPIO.setmode(GPIO.BCM)
input_channel = 17
relay_channel = 22
GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay_channel, GPIO.OUT)

toggle = 0
while True:
    if GPIO.input(input_channel):
        if toggle == 0:
            print("BUTTON: released\n")
        toggle=1
    else:
        print("BUTTON: pressed")
        print("MAIN LIGHTS: off")
        print("DISCO BALL: on")
        print("DISCO LIGHT: on")
        print("MUSIC: on")
        GPIO.output(relay_channel, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(relay_channel, GPIO.LOW)
        print("PARTY: off")
        print("MAIN LIGHTS: on")
        toggle=0

