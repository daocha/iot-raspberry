import RPi.GPIO as gpio
import time
from dcha.raspberry.functions import Action as act

gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_UP)

print("initializing...")

def light_callback(channel):
    print("Light detected...")
    #act.sendEmail()

def shock_callback(channel):
    print("Shock detected...")
    #act.sendEmail()

try:
    print("adding event listeners")
    #26 for light sensor
    gpio.add_event_detect(26, gpio.RISING, callback=light_callback, bouncetime=3000)
    #24 for shock sensor
    gpio.add_event_detect(24, gpio.RISING, callback=shock_callback, bouncetime=1000)

    while True:
        time.sleep(1)
except:
    gpio.cleanup()