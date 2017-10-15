import time

import RPi.GPIO as gpio
from actions.functions import Action as act


gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_UP)

print("initializing...")

def lighton_callback(channel):
    print("Light detected...")
    act.updateThing('True', None)

def lightoff_callback(channel):
    print("Light detected...")
    act.updateThing('False', None)

def shockon_callback(channel):
    print("Shocking detected...")
    act.updateThing(None, 'True')
    
def shockoff_callback(channel):
    print("Shocking detected...")
    act.updateThing(None, 'False')

def main():
    try:
        print("adding event listeners")
        # 26 for light sensor: light on
        gpio.add_event_detect(26, gpio.RISING, callback=lighton_callback, bouncetime=3000)
        
        # 26 for light sensor: light off
        gpio.add_event_detect(26, gpio.FALLING, callback=lightoff_callback, bouncetime=3000)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.RISING, callback=shockon_callback, bouncetime=1000)
        
        # 24 for shock sensor: stop shocking
        gpio.add_event_detect(24, gpio.FALLING, callback=shockoff_callback, bouncetime=1000)
        
        act.listenDelta()
    
        while True:
            time.sleep(1)
    except:
        gpio.cleanup()

if __name__ == "__main__":
    main()
