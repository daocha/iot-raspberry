import time

import RPi.GPIO as gpio
from actions.functions import Action as act


gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
gpio.setup(26, gpio.IN)

print("initializing...")

def light_callback(channel):
    print("Light detected...")
    if gpio.input(channel):
        act.updateThing('True', None)
    else:
        act.updateThing('False', None)

def shock_callback(channel):
    print("Shocking detected...")
    if gpio.input(channel):
        act.updateThing(None, 'True')
    else:
        act.updateThing(None, 'False')

def main():
    try:
        print("adding event listeners")
        # 26 for light sensor: light on
        gpio.add_event_detect(26, gpio.BOTH, callback=light_callback, bouncetime=3000)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.BOTH, callback=shock_callback, bouncetime=1000)
        
        act.listenDelta()
    
        while True:
            time.sleep(1)
    except:
        gpio.cleanup()

if __name__ == "__main__":
    main()
