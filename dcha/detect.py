'''
/*
 * Listener Raspberry Pi GPIO
 * <p>
 * Push to AWS IoT 
 */
 '''

import time

import RPi.GPIO as gpio
import sys,traceback
from actions.functions import Action as act


gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
gpio.setup(26, gpio.IN)

print("initializing...")

global lighton, lighton_new, shocking, shocking_new
lighton = False
lighton_new = False
shocking = False
shocking_new = False

def light_callback(channel):
    onoff = gpio.input(channel)
    print("Light detected, value = " + str(onoff))
    global lighton, lighton_new
    if onoff:
        lighton_new = True
    else:
        lighton_new = False
    
    

def shock_callback(channel):
    onoff = gpio.input(channel)
    print("Shocking detected, value = " + str(onoff))
    global shocking, shocking_new
    shocking_new = True
    time.sleep(10)
    shocking_new = False

def status_checking():
    print("status checking...")
    global lighton, lighton_new, shocking, shocking_new
    if lighton ^ lighton_new:
        act.updateThing(str(lighton_new), None)
        lighton = lighton_new
    if shocking ^ shocking_new:
        act.updateThing(None, str(shocking_new))
        shocking = shocking_new
    act.listenDelta()

def main():
    try:
        print("adding event listeners")
        # 26 for light sensor: light on
        gpio.add_event_detect(26, gpio.BOTH, callback=light_callback, bouncetime=500)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.RISING, callback=shock_callback, bouncetime=500)
        
        while True:
            status_checking()
            time.sleep(5)
    except:
        traceback.print_exc(file=sys.stdout)
        gpio.cleanup()

if __name__ == "__main__":
    main()
