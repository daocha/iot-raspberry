import time

import RPi.GPIO as gpio
from actions.functions import Action as act


gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
gpio.setup(26, gpio.IN)

print("initializing...")

lighton = False
lighton_new = False
shocking = False
shocking_new = False

def light_callback(channel):
    onoff = gpio.input(channel)
    print("Light detected, value = " + onoff)
    if onoff:
        lighton_new = True
    else:
        lighton_new = False
    
    

def shock_callback(channel):
    onoff = gpio.input(channel)
    print("Shocking detected, value = " + onoff)
    shocking_new = True
    time.sleep(10)
    shocking_new = False
    

def main():
    try:
        print("adding event listeners")
        # 26 for light sensor: light on
        gpio.add_event_detect(26, gpio.BOTH, callback=light_callback, bouncetime=200)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.RISING, callback=shock_callback, bouncetime=200)
        
        act.listenDelta()
    
        while True:
            if not lighton ^ lighton_new:
                act.updateThing(str(lighton_new), None)
                lighton = lighton_new
            
            if not shocking ^ shocking_new:
                act.updateThing(None, str(shocking_new))
                shocking = shocking_new
                
            time.sleep(5)
    except:
        gpio.cleanup()

if __name__ == "__main__":
    main()
